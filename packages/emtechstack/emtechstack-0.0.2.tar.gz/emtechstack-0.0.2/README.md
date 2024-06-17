
# Emtechstack

Emtechstack is a CLI tool designed to manage Docker-based development environments with Conda support. It allows you to initialize profiles, start and stop infrastructure, and manage Conda environments effortlessly.

## Features

- **Initialize Profiles**: Clone a repository and set up the necessary directory structure without `.git` files.
- **Manage Docker Infrastructure**: Start and stop Docker containers using `docker-compose`.
- **Manage API**: Start and stop a FastAPI application.
- **Build Conda Environments**: Create and activate Conda environments, and install dependencies from `requirements.txt`.

## Installation

You can install Emtechstack using pip:

```sh
pip install emtechstack
```

## Usage

### Initialize a Profile

Clone a repository and set up the necessary directory structure without `.git` files:

```sh
emtechstack init --profile <GitHub-user>/<repo>
```

For example:

```sh
emtechstack init --profile user/repo
```

### Navigate to the Profile Directory

After initializing the profile, navigate to the profile directory:

```sh
cd repo
```

### Start the Infrastructure

Start the infrastructure using Docker Compose:

```sh
emtechstack start_infra
```

### Stop the Infrastructure

Stop the infrastructure using Docker Compose:

```sh
emtechstack stop_infra
```

### Start the API

Start the FastAPI application:

```sh
emtechstack start_api
```

### Stop the API

Stop the FastAPI application:

```sh
emtechstack stop_api
```

### Build and Activate a Conda Environment

Create and activate a Conda environment, and install dependencies from `requirements.txt`:

```sh
emtechstack build --name <env-name>
```

For example:

```sh
emtechstack build --name myenv
```

## Commands and Options

### `emtechstack init`

Initialize the profile by cloning the repository.

```
Usage: emtechstack init --profile <profile-path>

Options:
  --profile  Profile path to initialize  [required]
```

### `emtechstack start_infra`

Start the infrastructure using `docker-compose up -d`.

```
Usage: emtechstack start_infra
```

### `emtechstack stop_infra`

Stop the infrastructure using `docker-compose down`.

```
Usage: emtechstack stop_infra
```

### `emtechstack start_api`

Start the FastAPI application.

```
Usage: emtechstack start_api
```

### `emtechstack stop_api`

Stop the FastAPI application.

```
Usage: emtechstack stop_api
```

### `emtechstack build`

Build and activate the Conda environment, and install dependencies from `requirements.txt`.

```
Usage: emtechstack build --name <env-name>

Options:
  --name  Name of the Conda environment to create and activate  [required]
```

## Contributing

If you would like to contribute to Emtechstack, please submit a pull request or open an issue on GitHub.

## License

This project is licensed under the MIT License.
