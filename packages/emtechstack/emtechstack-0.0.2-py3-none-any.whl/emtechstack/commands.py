import os
import shutil
import subprocess
import requests
import zipfile
from io import BytesIO

def init_profile(profile):
    repo_url = f'https://github.com/{profile}/archive/refs/heads/main.zip'
    response = requests.get(repo_url)
    if response.status_code == 200:
        zip_file = zipfile.ZipFile(BytesIO(response.content))
        dest_dir = os.path.join(os.getcwd(), profile.split('/')[-1])
        os.makedirs(dest_dir, exist_ok=True)
        for file in zip_file.namelist():
            if not file.startswith(f'{profile.split("/")[-1]}-main/.git'):
                zip_file.extract(file, dest_dir)
        print(f"Initialized profile at {dest_dir}")
    else:
        print(f"Failed to download profile from {repo_url}")

def start_infra():
    subprocess.run(['docker-compose', 'up', '-d'], check=True)
    print("Infrastructure started")

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
