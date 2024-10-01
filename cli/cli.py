import click
import requests
import json
from config import API_URL


@click.group()
def cli():
    """CLI for interacting with the CI/CD Pipeline API."""
    pass


@click.command()
@click.argument("pipeline_id", type=int)
def get_pipeline(pipeline_id):
    """Retrieve the configuration of an existing pipeline by ID."""
    response = requests.get(f"{API_URL}/pipelines/{pipeline_id}")
    if response.status_code == 200:
        click.echo(response.json())
    else:
        click.echo(f"Error: {response.status_code} - {response.text}")


@click.command()
@click.argument("pipeline_id", type=int)
def trigger_pipeline(pipeline_id):
    """Trigger the execution of a pipeline."""
    response = requests.post(f"{API_URL}/pipelines/{pipeline_id}/trigger")
    if response.status_code == 200:
        click.echo(response.json())
    else:
        click.echo(f"Error: {response.status_code} - {response.text}")


@click.command()
@click.argument("pipeline_id", type=int)
@click.argument("pipeline_data", type=str)
def update_pipeline(pipeline_id, pipeline_data):
    """Update an existing pipeline configuration."""
    data = json.loads(pipeline_data)
    response = requests.put(f"{API_URL}/pipelines/{pipeline_id}", json=data)
    if response.status_code == 200:
        click.echo(response.json())
    else:
        click.echo(f"Error: {response.status_code} - {response.text}")


@click.command()
@click.argument("pipeline_data", type=str)
def create_pipeline(pipeline_data):
    """Create a new CI/CD pipeline configuration."""
    data = json.loads(pipeline_data)
    headers = {"Content-Type": "application/json"}
    response = requests.post(f"{API_URL}/pipelines", json=data, headers=headers)
    if response.status_code == 201:
        click.echo(response.json())
    else:
        click.echo(f"Error: {response.status_code} - {response.text}")
        if response.status_code == 403:
            click.echo("Forbidden: You don't have permission to access this resource.")


@click.command()
@click.argument("pipeline_id", type=int)
def delete_pipeline(pipeline_id):
    """Delete a pipeline configuration."""
    response = requests.delete(f"{API_URL}/pipelines/{pipeline_id}")
    if response.status_code == 200:
        click.echo(response.json())
    else:
        click.echo(f"Error: {response.status_code} - {response.text}")


@click.command()
def help():
    """Show this message and exit."""
    click.echo(cli.get_help(click.Context(cli)))


cli.add_command(get_pipeline)
cli.add_command(trigger_pipeline)
cli.add_command(update_pipeline)
cli.add_command(create_pipeline)
cli.add_command(delete_pipeline)
cli.add_command(help)

if __name__ == "__main__":
    cli()
