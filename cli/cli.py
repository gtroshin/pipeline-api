import click
import requests
import json
import os
from cli.config import API_URL

API_KEY = os.getenv("API_KEY")


def get_headers(api_key):
    if not api_key:
        raise click.ClickException(
            "API key is required. Set the API_KEY environment variable or pass it as '--api-key' argument."
        )
    return {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}


@click.group()
def cli():
    """CLI for interacting with the CI/CD Pipeline API."""
    pass


@click.command()
@click.argument("pipeline_id", type=int)
@click.option("--api-key", default=API_KEY, help="API key for authentication")
def get_pipeline(pipeline_id, api_key):
    """Retrieve the configuration of pipeline by ID."""
    headers = get_headers(api_key)
    response = requests.get(f"{API_URL}/pipelines/{pipeline_id}", headers=headers)
    if response.status_code == 200:
        click.echo(response.json())
    elif response.status_code == 404:
        click.echo("Error: Pipeline not found.")
    else:
        click.echo(f"Error: {response.status_code} - {response.text}")


@click.command()
@click.argument("pipeline_id", type=int)
@click.option("--api-key", default=API_KEY, help="API key for authentication")
def trigger_pipeline(pipeline_id, api_key):
    """Trigger the execution of a pipeline."""
    headers = get_headers(api_key)
    response = requests.post(
        f"{API_URL}/pipelines/{pipeline_id}/trigger", headers=headers
    )
    if response.status_code == 200:
        click.echo(response.json())
    elif response.status_code == 404:
        click.echo("Error: Pipeline not found.")
    else:
        click.echo(f"Error: {response.status_code} - {response.text}")


@click.command()
@click.argument("pipeline_id", type=int)
@click.argument("pipeline_data", type=str)
@click.option("--api-key", default=API_KEY, help="API key for authentication")
def update_pipeline(pipeline_id, pipeline_data, api_key):
    """Update an existing pipeline configuration."""
    try:
        data = json.loads(pipeline_data)
    except json.JSONDecodeError:
        click.echo("Error: Invalid JSON format.")
        return

    headers = get_headers(api_key)
    response = requests.put(
        f"{API_URL}/pipelines/{pipeline_id}", json=data, headers=headers
    )
    if response.status_code == 200:
        click.echo(response.json())
    elif response.status_code == 404:
        click.echo("Error: Pipeline not found.")
    elif response.status_code == 400:
        click.echo(f"Error: {response.json().get('error', 'Invalid input')}")
    else:
        click.echo(f"Error: {response.status_code} - {response.text}")


@click.command()
@click.argument("pipeline_data", type=str)
@click.option("--api-key", default=API_KEY, help="API key for authentication")
def create_pipeline(pipeline_data, api_key):
    """Create a new CI/CD pipeline configuration."""
    try:
        data = json.loads(pipeline_data)
    except json.JSONDecodeError:
        click.echo("Error: Invalid JSON format.")
        return

    headers = get_headers(api_key)
    response = requests.post(f"{API_URL}/pipelines", json=data, headers=headers)
    if response.status_code == 201:
        click.echo(response.json())
    elif response.status_code == 400:
        click.echo(f"Error: {response.json().get('error', 'Invalid input')}")
    elif response.status_code == 403:
        click.echo("Forbidden: You don't have permission to access this resource.")
    else:
        click.echo(f"Error: {response.status_code} - {response.text}")


@click.command()
@click.argument("pipeline_id", type=int)
@click.option("--api-key", default=API_KEY, help="API key for authentication")
def delete_pipeline(pipeline_id, api_key):
    """Delete a pipeline configuration."""
    headers = get_headers(api_key)
    response = requests.delete(f"{API_URL}/pipelines/{pipeline_id}", headers=headers)
    if response.status_code == 200:
        click.echo(response.json())
    elif response.status_code == 404:
        click.echo("Error: Pipeline not found.")
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
