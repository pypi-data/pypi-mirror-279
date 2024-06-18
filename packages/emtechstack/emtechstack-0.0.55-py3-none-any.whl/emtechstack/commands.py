import os
import shutil
import subprocess
import requests
import zipfile
import yaml
from io import BytesIO
from tabulate import tabulate
from termcolor import colored
import pkg_resources  # to retrieve the package version
import signal


def init_profile(profile, name=None):
    repo_url = "https://github.com/emtechstack/infra-profiles/archive/refs/heads/main.zip"
    temp_dir = "emtechstack_temp_profile_download"

    try:
        # Step 1: Download the repo
        response = requests.get(repo_url)
        if response.status_code != 200:
            print(f"Failed to download profile from {repo_url}")
            return

        # Step 2: Unzip the repo
        zip_file = zipfile.ZipFile(BytesIO(response.content))
        zip_file.extractall(temp_dir)

        profile_path = os.path.join(temp_dir, "infra-profiles-main", "profiles", profile)
        if not os.path.exists(profile_path):
            print(f"Profile '{profile}' not found in the repository.")
            return

        # Step 3: Create the destination directory
        repo_name = name if name else profile
        dest_dir = os.path.join(os.getcwd(), repo_name)

        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

        # Copy all files and directories from the profile directory to the destination directory
        for root, dirs, files in os.walk(profile_path):
            relative_path = os.path.relpath(root, profile_path)
            dest_path = os.path.join(dest_dir, relative_path)
            
            if not os.path.exists(dest_path):
                os.makedirs(dest_path)
            
            for file in files:
                src_file = os.path.join(root, file)
                shutil.copy(src_file, dest_path)

        # Step 5: Clean up the downloaded zip and extracted files
        shutil.rmtree(temp_dir)
        print(f"Initialized profile at {dest_dir}")

    except Exception as e:
        print(f"An error occurred: {e}")
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def find_and_kill_processes(port="8000"):
    try:
        # Identify the platform
        if os.name == "nt":  # Windows
            command = f"netstat -ano | findstr :{port}"
            processes = subprocess.check_output(command, shell=True).decode()
            for line in processes.strip().split("\n"):
                if line:
                    parts = line.split()
                    pid = parts[-1]
                    kill_command = f"taskkill /F /PID {pid}"
                    subprocess.run(kill_command, shell=True, check=True)
            print(f"Processes running on port {port} have been killed.")
        else:  # Unix-like systems (Linux, macOS)
            command = f"lsof -i :{port} | grep LISTEN"
            processes = subprocess.check_output(command, shell=True).decode()
            for line in processes.strip().split("\n"):
                if line:
                    parts = line.split()
                    pid = int(parts[1])
                    os.kill(pid, signal.SIGKILL)
            print(f"Processes running on port {port} have been killed.")
    except subprocess.CalledProcessError as e:
        print(f"No processes found running on port {port}: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


def start_infra():
    subprocess.run(["docker-compose", "up", "-d"], check=True)
    print("Infrastructure started")
    display_services()


def stop_infra():
    try:
        subprocess.run(["docker-compose", "down"], check=True)
        # display_services()
        print("Infrastructure stopped")

    except subprocess.CalledProcessError as e:
        print(
            colored(f"An error occurred while starting the infrastructure: {e}", "red")
        )
        print(colored(f"Command: {e.cmd}", "red"))
        print(colored(f"Return code: {e.returncode}", "red"))
        print(colored(f"Output: {e.output}", "red"))


PID_FILE = "api_server.pid"


def start_api(port="8000"):
    try:
        # Start the API server
        # process = subprocess.Popen(['uvicorn', 'api:app', '--host', '0.0.0.0', '--port', port, '--reload'])
        process = subprocess.Popen(
            ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", port]
        )
        print("API started")

        # Save the process ID to a file
        with open(PID_FILE, "w") as pid_file:
            pid_file.write(str(process.pid))
    except PermissionError:
        print("Permission denied: Unable to write PID file.")
    except Exception as e:
        print(f"An error occurred while starting the API: {e}")


def stop_api():
    if os.path.exists(PID_FILE):
        try:
            with open(PID_FILE, "r") as pid_file:
                pid = int(pid_file.read())

            try:
                # Check if the process is running
                os.kill(pid, 0)
            except OSError:
                print("No API process found")
            else:
                # If the process is running, terminate it
                os.kill(pid, signal.SIGTERM)
                print("API stopped")

            # Remove the PID file
            os.remove(PID_FILE)
        except PermissionError:
            print("Permission denied: Unable to read or remove PID file.")
        except Exception as e:
            print(f"An error occurred while stopping the API: {e}")
    else:
        print("No PID file found. API might not be running.")


def build_env(name=None):
    try:
        if name is None:
            name = os.path.basename(os.getcwd())

        # Create the Conda environment
        subprocess.run(["conda", "create", "-n", name, "python=3.8", "-y"], check=True)
        print(f"Conda environment '{name}' created")

        # Write a temporary shell script to activate the environment and install requirements
        script_content = f"""
        #!/bin/bash
        source $(conda info --base)/etc/profile.d/conda.sh
        conda activate {name}
        pip install -r requirements.txt
        """
        script_path = "temp_script.sh"
        with open(script_path, "w") as script_file:
            script_file.write(script_content)

        # Make the script executable
        os.chmod(script_path, 0o775)

        # Run the script using /bin/bash
        subprocess.run(["/bin/bash", script_path], check=True)

        # Clean up the temporary script
        os.remove(script_path)

        print(f"Conda environment '{name}' activated and requirements installed")
        # display_services()

    except subprocess.CalledProcessError as e:
        print(f"An error occurred while building the environment: {e}")


def update_emtechstack():
    try:
        # Get the current version
        current_version = pkg_resources.get_distribution("emtechstack").version

        # Upgrade the package
        result = subprocess.run(
            ["pip", "install", "--upgrade", "emtechstack"],
            check=True,
            capture_output=True,
            text=True,
        )
        # print(result.stdout)  # Optional: Print the output of the command

        # Reload the package metadata
        pkg_resources.working_set = pkg_resources.WorkingSet()

        # Get the new version
        new_version = pkg_resources.get_distribution("emtechstack").version

        # Print the update message
        if current_version != new_version:
            print(
                colored(
                    f"emtechstack has been updated: version {current_version} -> {new_version} ✔",
                    "green",
                )
            )
        else:
            print(
                colored(
                    f"emtechstack is already at the latest version: {new_version} ✔",
                    "green",
                )
            )
    except subprocess.CalledProcessError as e:
        print(colored(f"An error occurred while updating emtechstack: {e}", "red"))
        print(colored(e.stdout, "red"))
        print(colored(e.stderr, "red"))
    except Exception as e:
        print(colored(f"An error occurred: {e}", "red"))


def display_services():
    try:
        with open("docker-compose.yml", "r") as file:
            docker_compose = yaml.safe_load(file)

        services = docker_compose.get("services", {})
        table_data = []

        for service, details in services.items():
            ports = details.get("ports", [])
            for port in ports:
                table_data.append([service, port.split(":")[0], port.split(":")[1]])

        if table_data:
            # Retrieve the package version
            version = pkg_resources.get_distribution("emtechstack").version

            # Prepare the title row
            title = f"EmTechStack AI Dev Tools (Version {version})"

            # Print the table with title as the first row
            table = tabulate(
                table_data,
                headers=["Service", "Port Local", "Port Docker"],
                tablefmt="grid",
            )
            title_line = "+" + "-" * (len(table.split("\n")[0]) - 2) + "+"
            title_row = f"| {title.center(len(title_line) - 4)} |"
            full_table = f"{title_line}\n{title_row}\n{table}"

            print(colored(full_table, "green"))
        else:
            print(colored("No services found in the docker-compose.yml file.", "red"))

    except FileNotFoundError:
        print(colored("docker-compose.yml file not found.", "red"))
    except yaml.YAMLError as exc:
        print(colored(f"Error reading docker-compose.yml file: {exc}", "red"))
    except pkg_resources.DistributionNotFound:
        print(
            colored(
                "emtechstack package not found. Ensure it is installed properly.", "red"
            )
        )

def update_requirements():
    try:
        # Read the existing requirements.txt file
        with open('requirements.txt', 'r') as file:
            requirements = file.readlines()

        # Clean and sort the requirements
        requirements = [req.strip() for req in requirements if req.strip()]
        requirements.sort()

        # Get the installed versions
        installed_packages = {pkg.key: pkg.version for pkg in pkg_resources.working_set}

        # Create a list to store updated requirements
        updated_requirements = []

        for req in requirements:
            package_name = req.split('==')[0].strip()
            if package_name in installed_packages:
                version = installed_packages[package_name]
                updated_requirements.append(f"{package_name}=={version}")
            else:
                updated_requirements.append(req)

        # Sort the updated requirements
        updated_requirements.sort()

        # Write the updated requirements back to requirements.txt
        with open('requirements.txt', 'w') as file:
            file.write("\n".join(updated_requirements) + "\n")

        print("requirements.txt has been updated with installed package versions.")

    except Exception as e:
        print(f"An error occurred: {e}")

def clean_code():
    subprocess.run(["black", "."], check=True)
