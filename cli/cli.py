import click
import requests

API_URL = "http://localhost:5000"


@click.group()
def cli():
    pass


@click.command()
@click.argument("pipeline_id")
def get_pipeline(pipeline_id):
    response = requests.get(f"{API_URL}/pipelines/{pipeline_id}")
    click.echo(response.json())


@click.command()
@click.argument("pipeline_id")
def trigger_pipeline(pipeline_id):
    response = requests.post(f"{API_URL}/pipelines/{pipeline_id}/trigger")
    click.echo(response.json())


cli.add_command(get_pipeline)
cli.add_command(trigger_pipeline)

if __name__ == "__main__":
    cli()
