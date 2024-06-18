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
    temp_dir = 'emtechstack_temp_profile_download'
    
    try:
        # Step 1: Download the repo
        response = requests.get(repo_url)
        if response.status_code != 200:
            print(f"Failed to download profile from {repo_url}")
            return
        
        # Step 2: Unzip the repo
        zip_file = zipfile.ZipFile(BytesIO(response.content))
        zip_file.extractall(temp_dir)
        
        profile_path = os.path.join(temp_dir, 'infra-profiles-main', 'profiles', profile)
        if not os.path.exists(profile_path):
            print(f"Profile '{profile}' not found in the repository.")
            return
        
        # Step 3: Create the destination directory
        repo_name = name if name else profile
        dest_dir = os.path.join(os.getcwd(), repo_name)
        
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        
        # Copy all files from the profile directory to the destination directory
        for root, dirs, files in os.walk(profile_path):
            for file in files:
                src_file = os.path.join(root, file)
                shutil.move(src_file, dest_dir)
        
        # Step 5: Clean up the downloaded zip and extracted files
        shutil.rmtree(temp_dir)
        print(f"Initialized profile at {dest_dir}")
    
    except Exception as e:
        print(f"An error occurred: {e}")
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


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