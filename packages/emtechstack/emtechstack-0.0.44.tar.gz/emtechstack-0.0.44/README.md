
# EmTechStack

Welcome to EmTechStack! 🎉 EmTechStack is a CLI tool designed to streamline the setup and management of your AI development environments. It allows you to easily manage Docker-based infrastructures, create and activate Conda environments, and handle your FastAPI applications.

## Features

- 🚀 **Initialize Profiles**: Clone a profile from the repository and set up the necessary directory structure.
- 🐳 **Manage Docker Infrastructure**: Start and stop Docker containers using `docker-compose`.
- ⚙️ **Manage API**: Start and stop a FastAPI application.
- 📦 **Build Conda Environments**: Create and activate Conda environments, and install dependencies from `requirements.txt`.
- 🧹 **Clean Code**: Use `black` to clean the codebase.
- 🔄 **Update EmTechStack**: Easily update the EmTechStack package to the latest version.

## Installation

Before you begin, ensure you have the following requirements installed:

1. [Python 3.10+](https://www.python.org/downloads/)
2. [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
3. [Docker](https://docs.docker.com/get-docker/)

### Step-by-Step Guide

1. **Install EmTechStack**

    ```sh
    pip install emtechstack
    ```

2. **Initialize a Profile**

    ```sh
    emtechstack init --profile <profile-name> [--name <custom-dir>]
    ```

    Example:

    ```sh
    emtechstack init --profile profile-name
    emtechstack init --profile profile-name --name custom-dir
    ```

3. **Navigate to the Profile Directory**

    ```sh
    cd profile-name
    ```

    Or if you specified a custom name:

    ```sh
    cd custom-dir
    ```

4. **Build and Activate a Conda Environment**

    ```sh
    emtechstack build --name <env-name>
    ```

    Example:

    ```sh
    emtechstack build --name myenv
    ```

5. **Start the Infrastructure**

    ```sh
    emtechstack start_infra
    ```

6. **Stop the Infrastructure**

    ```sh
    emtechstack stop_infra
    ```

7. **Start the API**

    ```sh
    emtechstack start_api --port 8000
    ```

8. **Stop the API**

    ```sh
    emtechstack stop_api
    ```

9. **Clean the Code**

    ```sh
    emtechstack clean
    ```

10. **Update EmTechStack**
    Make sure you have the latest version of the CLI tool before start your day ☕☕

    ```sh
    emtechstack update
    ```

## Issues and Contributions

If you face any issues or have suggestions, feel free to open a new issue in the [GitHub repository](https://github.com/emtechstack/emtechstack/issues). We welcome contributions! 

⭐ Please star the repo if you find it helpful. ⭐

Thank you for using EmTechStack!
