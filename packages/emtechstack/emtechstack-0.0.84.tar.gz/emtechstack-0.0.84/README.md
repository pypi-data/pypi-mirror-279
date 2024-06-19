
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
    pip install --upgrade emtechstack
    ```

    If you have already installed the cli please make sure its updated by:

    ```sh
    emtechstack update
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

    Then activate the conda env which built automatically for you for start developing. The env is ready to used and equipped with necessary libraries.

    ```sh
    conda activate myenv
    ```

5. **Start the Infrastructure**

    ```sh
    emtechstack start-infra
    ```

6. **Stop the Infrastructure**

    ```sh
    emtechstack stop-infra
    ```

7. **Start the API**

    ```sh
    emtechstack start-api --port 8000
    ```

8. **Stop the API**

    ```sh
    emtechstack stop-api
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


## Command Reference

| Command                        | Description                                                         |
|--------------------------------|---------------------------------------------------------------------|
| `emtechstack build`            | Build and activate the Conda environment, and...                    |
| `emtechstack clean`            | Clean the code using black                                          |
| `emtechstack clean-port`       | Clean the port                                                      |
| `emtechstack goodnight`        | Gracefully shutdown the API and Infra application                   |
| `emtechstack graceful-shutdown`| Gracefully shutdown the API and Infra application                   |
| `emtechstack init`             | Initialize the profile by cloning the repo                          |
| `emtechstack start-api`        | Start the FastAPI application                                       |
| `emtechstack start-infra`      | Start the infrastructure using docker-compose                       |
| `emtechstack stop-api`         | Stop the FastAPI application                                        |
| `emtechstack stop-infra`       | Stop the infrastructure using docker-compose                        |
| `emtechstack update`           | Update the emtechstack package                                      |
| `emtechstack update-requirements`| Update the requirements.txt file with installed dependencies       |
| `emtechstack upgrade`          | Update the emtechstack package                                      |
| `emtechstack version`          | Show the current version of EmTechStack                             |



## Issues and Contributions

If you face any issues or have suggestions, feel free to open a new issue in the [GitHub repository](https://github.com/emtechstack/emtechstack/issues). We welcome contributions!

⭐ Please star the repo if you find it helpful. ⭐

Built with ❤️ by Dev for Devs

Thank you for using EmTechStack!
