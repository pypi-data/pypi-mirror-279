import click
from emtechstack.commands import init_profile, start_infra, stop_infra, start_api, stop_api, build_env

@click.group()
def cli():
    """Emtechstack CLI Tool"""
    pass

@cli.command()
@click.option('--profile', required=True, help='Profile path to initialize')
def init(profile):
    """Initialize the profile by cloning the repo"""
    init_profile(profile)

@cli.command()
def start_infra():
    """Start the infrastructure using docker-compose"""
    start_infra()

@cli.command()
def stop_infra():
    """Stop the infrastructure using docker-compose"""
    stop_infra()

@cli.command()
def start_api():
    """Start the FastAPI application"""
    start_api()

@cli.command()
def stop_api():
    """Stop the FastAPI application"""
    stop_api()

@cli.command()
@click.option('--name', required=True, help='Name of the Conda environment to create and activate')
def build(name):
    """Build and activate the Conda environment, and install dependencies from requirements.txt"""
    build_env(name)

if __name__ == '__main__':
    cli()
