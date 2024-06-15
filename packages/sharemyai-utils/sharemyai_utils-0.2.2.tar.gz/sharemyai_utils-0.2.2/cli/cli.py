import asyncio
import datetime
import json
import os
import shutil
import signal
import time
import click
import requests
import logging
import psutil
import tqdm
from tenacity import retry, stop_after_attempt, wait_exponential

from cli.fingerprint import get_fingerprint
from cli.lib import create_venv, get_and_download_plugin, get_current_user, get_inference_job, get_my_workers, install_requirements, install_sharemyai_utils, install_torch_requirements, kill_process_on_port, login_with_token, post_register_worker, process_inference_job, run_plugin

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@click.group()
def cli():
    pass

@click.command(help="Share my AI CLI - Help")
def help():
    click.echo(f'Help:')
    click.echo(f'  - help: Show this help message')
    return

@click.command(help="Login with a token")
@click.option('--token', required=True, help='Your login token')
def login(token):
    logged_in_user = login_with_token(token)
    if not logged_in_user:
        click.echo('Login failed, please try again.')
        return
    click.echo(f'Logged in successfully as {logged_in_user["name"]} - {logged_in_user["id"]}')
    return

@click.command(help="Get the current user")
def current_user():
    user = get_current_user()
    formatted_json = json.dumps(user, indent=4, sort_keys=True)
    click.echo(f'Current user:\n{formatted_json}')
    return

@click.command(help="Get the current machines fingerprint")
def fingerprint():
    fingerprint_bytes = asyncio.run(get_fingerprint())
    fingerprint_str = fingerprint_bytes.hex()
    click.echo(f'Fingerprint: {fingerprint_str}')
    return

@click.command(help="Register new worker")
@click.option('--plugin_id', required=True, help='The plugin id to work on')
def register_worker(plugin_id):
    worker = post_register_worker(plugin_id)
    formatted_json = json.dumps(worker, indent=4, sort_keys=True)
    click.echo(f'Worker:\n{formatted_json}')
    return

@click.command(help="Get my workers")
def my_workers():
    workers = get_my_workers()
    formatted_json = json.dumps(workers, indent=4, sort_keys=True)
    click.echo(f'Workers:\n{formatted_json}')
    return

@click.command(help="Run worker")
@click.option('--plugin_id', required=True, help='The plugin id to work on')
def run_worker(plugin_id):
    # first, register a worker
    worker = post_register_worker(plugin_id)
    formatted_json = json.dumps(worker, indent=4, sort_keys=True)
    click.echo(f'Worker:\n{formatted_json}')
    # then, download the plugin
    plugin, plugin_path = get_and_download_plugin(plugin_id)
    click.echo(f'Plugin downloaded to {plugin_path}')
    # then, create a venv for the plugin
    venv_path = create_venv(plugin_path)
    click.echo(f'Venv created at {venv_path}')
    # then, install the plugin requirements
    install_torch_requirements(venv_path, plugin['torchRequirements'])
    install_requirements(venv_path, plugin['requirements'])
    click.echo(f'Requirements installed')
    # then, run the plugin
    pid = run_plugin(venv_path, plugin_path, plugin['name'])
    try:
        while True:
            with click.progressbar(length=0, label='Checking for jobs', show_eta=False, show_pos=True) as bar:
                while True:
                    job = get_inference_job(worker['id'])
                    if not job:
                        bar.update(0)
                        bar.label = f'No job found - {datetime.datetime.now()}...'
                        time.sleep(5)
                        continue
                    bar.label = f'Job found: {job}'
                    break
            # process it 
            process_inference_job(
                job['params'].get('prompt', ''),
                job['params'].get('image', ''),
                job['params'],
                plugin['params'],
                job['id']
            )
            time.sleep(5)
    except KeyboardInterrupt:
        click.echo(f'Stopping plugin - {datetime.datetime.now()}...')
        try:
            os.kill(pid, signal.SIGTERM)
        except ProcessLookupError:
            pass
    click.echo(f'Plugin stopped - {datetime.datetime.now()}...')
    return

PLUGIN_BASE_DIR = './plugin_cache'

@click.command(help="Run worker that will dynamically download and run plugins")
@click.option('--reset', default=False, help='Reset the worker')
def run_multiplugin_worker(reset):
    plugin_processes = {}

    # if we are resetting, delete all our downloaded plugins 
    if reset:
        for item in os.listdir(PLUGIN_BASE_DIR):
            item_path = os.path.join(PLUGIN_BASE_DIR, item)
            if os.path.isfile(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
        # delete plugin cache file if it exists
        if os.path.exists("cached_plugins.json"):
            os.remove("cached_plugins.json")
        # stop all plugins 
        kill_process_on_port(3030)
        click.echo(f'Deleted all downloaded plugins')
        return

    # first, register a worker
    worker = post_register_worker()
    formatted_json = json.dumps(worker, indent=4, sort_keys=True)
    click.echo(f'Worker:\n{formatted_json}')

    cached_plugins_file = "cached_plugins.json"
    if os.path.exists(cached_plugins_file):
        with open(cached_plugins_file, "r") as f:
            cached_plugins = json.load(f)
    else:
        cached_plugins = {"current": ""}

    while True:
        try:
            logger.info(f'Checking for jobs - {datetime.datetime.now()}...')

            @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
            def get_job():
                return get_inference_job(worker['id'])

            job = get_job()

            if not job:
                logger.info(f'No job found - {datetime.datetime.now()}...')
                time.sleep(5)
                continue

            logger.info(f'Job found: {job}')

            # get the plugin id from the job
            plugin_id = job['pluginId']

            # see if its in our cache, if it is, get its name 
            if plugin_id in cached_plugins:
                current_plugin_name = cached_plugins[plugin_id]['plugin']['name']
            else:
                current_plugin_name = ""

            is_current_plugin = False
            if current_plugin_name != "":
                # we can get our plugins name from the :3030/ route 
                try:
                    response = requests.get(f"http://localhost:3030/")
                    # the name is in the string, lowercase and compare 
                    is_current_plugin = lambda plugin_name: response.text.lower().includes(current_plugin_name.lower())
                except Exception as e:
                    pass

            if not is_current_plugin:
                # Kill the current running plugins 
                kill_process_on_port(3030)

                if plugin_id in cached_plugins:
                    # if the plugin is already cached, use the cached version
                    plugin = cached_plugins[plugin_id]['plugin']
                    plugin_path = cached_plugins[plugin_id]['plugin_path']
                    venv_path = cached_plugins[plugin_id]['venv_path']
                    click.echo(f'Using cached plugin: {plugin_id}')
                else:
                    # if the plugin is not cached, download and set it up
                    plugin, plugin_path = get_and_download_plugin(plugin_id, PLUGIN_BASE_DIR)
                    click.echo(f'Plugin downloaded to {plugin_path}')

                    venv_path = create_venv(plugin_path)
                    click.echo(f'Venv created at {venv_path}')

                    install_torch_requirements(venv_path, plugin['torchRequirements'])
                    install_requirements(venv_path, plugin['requirements'])
                    click.echo(f'Requirements installed')

                    # cache the plugin for future use
                    cached_plugins[plugin_id] = {
                        'plugin': plugin,
                        'plugin_path': plugin_path,
                        'venv_path': venv_path
                    }
                    # save the updated cached_plugins to file
                    with open(cached_plugins_file, "w") as f:
                        json.dump(cached_plugins, f)
                install_sharemyai_utils(venv_path)
                pid = run_plugin(venv_path, plugin_path, plugin['name'])
                plugin_processes[plugin_id] = pid
            else:
                venv_path = cached_plugins[plugin_id]['venv_path']
                plugin_path = cached_plugins[plugin_id]['plugin_path']
                plugin = cached_plugins[plugin_id]['plugin']
                
            # Run the plugin only if it's not already running
            #if plugin_id not in plugin_processes or not psutil.pid_exists(plugin_processes[plugin_id]):
            # Kill any existing process with the same name or port

            # wait till we get a response from our healthcheck endpoint
            while True:
                print('Waiting for healthcheck...')
                try:
                    response = requests.get(f"http://localhost:3030/healthcheck")
                except Exception as e:
                    print('Healthcheck failed, retrying in 5 seconds...')
                    time.sleep(5)
                    continue
                if response.status_code == 200:
                    print('Healthcheck passed, continuing...')
                    break
                print('Healthcheck failed, retrying in 5 seconds...')
                time.sleep(5)

            with tqdm.tqdm(desc=f'Processing job {job["id"]}', unit='step') as pbar:
                @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
                def process_job():
                    process_inference_job(
                        job['params'].get('prompt', ''),
                        job['params'].get('image', ''),
                        job['params'],
                        plugin['params'],
                        job['id']
                    )
                    pbar.update(1)

                process_job()

        except KeyboardInterrupt:
            logger.info(f'Stopping worker - {datetime.datetime.now()}...')
            break
        except Exception as e:
            logger.exception(f'Error occurred: {str(e)}')
            time.sleep(5)
            
    return

cli.add_command(help)
cli.add_command(login)
cli.add_command(current_user)
cli.add_command(fingerprint)
cli.add_command(register_worker)
cli.add_command(my_workers)
cli.add_command(run_worker)
cli.add_command(run_multiplugin_worker)



