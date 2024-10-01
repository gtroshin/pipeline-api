# CI/CD Pipeline API
![Python 3.8.0](https://img.shields.io/badge/Python-3.8.0-green.svg)
![Flask 3.0.3](https://img.shields.io/badge/Flask-3.0.3-blue.svg)

This is a simple CI/CD pipeline app built using Flask. It allows users to create, retrieve, update, delete, and trigger pipelines. This project also includes a CLI for interacting with the API.

## Prerequisites

- Python 3.8+

## Dependencies

You can install the dependencies using pip (it is highly recommended to use a virtual environment):

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

To deactivate the virtual environment, run:

```bash
deactivate
```

## Environment Variables

Create a `.env` file in root directory of project and add necessary environment variables (example):

```plaintext
API_KEY=api_key
API_URL=http://127.0.0.1:5000
```

## Running Tests

To run the unit tests, use the following command:

```bash
python -m unittest discover -s tests
```

## Running the API

To run the app locally, use the following command:

```bash
python run.py
```

The app will run on `http://127.0.0.1:5000`.

## App Example Usage

### Create a New Pipeline

```bash
curl -X POST http://127.0.0.1:5000/pipelines -H "Content-Type: application/json" -H "Authorization: Bearer api_key" -d '{
    "stages": [
        {
            "type": "run",
            "command": "echo \"Running tests\""
        },
        {
            "type": "build",
            "dockerfile": "Dockerfile"
        },
        {
            "type": "deploy",
            "manifest": "k8s/deployment.yaml"
        }
    ]
}'
```

### Update an Existing Pipeline

```bash
curl -X PUT http://127.0.0.1:5000/pipelines/1 -H "Content-Type: application/json" -H "Authorization: Bearer api_key" -d '{
    "stages": [
        {
            "type": "run",
            "command": "echo \"Running updated tests\""
        },
        {
            "type": "build",
            "dockerfile": "UpdatedDockerfile"
        },
        {
            "type": "deploy",
            "manifest": "k8s/updated_deployment.yaml"
        }
    ]
}'
```

### Retrieve an Existing Pipeline by ID

```bash
curl -X GET http://127.0.0.1:5000/pipelines/1 -H "Authorization: Bearer api_key"
```

### Trigger the Execution of a Pipeline

```bash
curl -X POST http://127.0.0.1:5000/pipelines/1/trigger -H "Authorization: Bearer api_key"
```

### Delete a Pipeline

```bash
curl -X DELETE http://127.0.0.1:5000/pipelines/1 -H "Authorization: Bearer api_key"
```

## Install `cicd-cli` CLI locally

Run the following command while at the project root to install the CLI:

```bash
pip install -e .
```

To uninstall the CLI, run:

```bash
pip uninstall cicd-cli
```

## CLI Example Usage

### Show help

```bash
cicd-cli help
```

### Create a New Pipeline

```bash
cicd-cli create-pipeline '{"stages": [{"type": "run", "command": "echo \"Running tests\""}, {"type": "build", "dockerfile": "Dockerfile"}, {"type": "deploy", "manifest": "k8s/deployment.yaml"}]}'
```

### Retrieve an Existing Pipeline by ID

```bash
cicd-cli get-pipeline 1
```

### Update an Existing Pipeline

```bash
cicd-cli update-pipeline 1 '{"stages": [{"type": "run", "command": "echo \"Running updated tests\""}, {"type": "build", "dockerfile": "UpdatedDockerfile"}, {"type": "deploy", "manifest": "k8s/updated_deployment.yaml"}]}'
```

### Trigger the Execution of a Pipeline

```bash
cicd-cli trigger-pipeline 1
```

### Delete a Pipeline

```bash
cicd-cli delete-pipeline 1
```
