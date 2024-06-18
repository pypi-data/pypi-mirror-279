import os
import shutil
import subprocess
import requests
import zipfile
import yaml
from io import BytesIO
from tabulate import tabulate
from termcolor import colored

def init_profile(profile, name=None):
    repo_url = 'https://github.com/emtechstack/infra-profiles/archive/refs/heads/main.zip'
    response = requests.get(repo_url)
    if response.status_code == 200:
        zip_file = zipfile.ZipFile(BytesIO(response.content))
        profile_path = f'infra-profiles-main/profiles/{profile}'
        repo_name = profile if name is None else name
        
        dest_dir = os.path.join(os.getcwd(), repo_name)
        
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        
        if not any(file.startswith(profile_path) for file in zip_file.namelist()):
            print(f"Profile '{profile}' not found in the repository.")
            return
        
        os.makedirs(dest_dir, exist_ok=True)
        for file in zip_file.namelist():
            if file.startswith(profile_path) and not file.endswith('/'):
                zip_file.extract(file, dest_dir)
        
        # Move files up one directory level
        src_dir = os.path.join(dest_dir, profile_path.split('/')[-1])
        for item in os.listdir(src_dir):
            shutil.move(os.path.join(src_dir, item), dest_dir)
        shutil.rmtree(src_dir)
        
        print(f"Initialized profile at {dest_dir}")
    else:
        print(f"Failed to download profile from {repo_url}")

def start_infra():
    subprocess.run(['docker-compose', 'up', '-d'], check=True)
    print("Infrastructure started")
    display_services()

def stop_infra():
    subprocess.run(['docker-compose', 'down'], check=True)
    print("Infrastructure stopped")

def start_api():
    subprocess.run(['uvicorn', 'app.main:app', '--host', '0.0.0.0', '--port', '8000', '--reload'], check=True)
    print("API started")

def stop_api():
    print("API stopped (implement actual stop logic as needed)")

def build_env(name):
    subprocess.run(['conda', 'create', '-n', name, 'python=3.8', '-y'], check=True)
    print(f"Conda environment '{name}' created")
    
    if os.name == 'nt':
        activate_command = f'conda activate {name} && pip install -r requirements.txt'
    else:
        activate_command = f'conda activate {name} && pip install -r requirements.txt'
    
    subprocess.run(activate_command, shell=True, check=True, executable="/bin/bash")
    print(f"Conda environment '{name}' activated and requirements installed")
    display_services()

def display_services():
    try:
        with open('docker-compose.yml', 'r') as file:
            docker_compose = yaml.safe_load(file)
        
        services = docker_compose.get('services', {})
        table_data = []
        
        for service, details in services.items():
            ports = details.get('ports', [])
            for port in ports:
                table_data.append([service, port])
        
        if table_data:
            print(colored(tabulate(table_data, headers=['Service', 'Port'], tablefmt='grid'), 'green'))
        else:
            print(colored("No services found in the docker-compose.yml file.", 'red'))
    
    except FileNotFoundError:
        print(colored("docker-compose.yml file not found.", 'red'))
    except yaml.YAMLError as exc:
        print(colored(f"Error reading docker-compose.yml file: {exc}", 'red'))

def clean_code():
    subprocess.run(['black', '.'], check=True)