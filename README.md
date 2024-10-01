# CI/CD Pipeline API

This is a simple CI/CD pipeline API built using Flask. It allows users to create, retrieve, update, delete, and trigger pipelines.

## Prerequisites

- Python 3.8+

## Dependencies

You can install the dependencies using pip:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

To deactivate the virtual environment, run:

```bash
deactivate
```

## Running the API

To run the API, use the following command:  

```bash 
python run.py
```

The API will run on `http://127.0.0.1:5000`.

## App Example Usage

### Create a New Pipeline

```bash
curl -X POST http://127.0.0.1:5000/pipelines -H "Content-Type: application/json" -d '{
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

### Retrieve an Existing Pipeline by ID

```bash
curl -X GET http://127.0.0.1:5000/pipelines/1
```

### Trigger the Execution of a Pipeline

```bash
curl -X POST http://127.0.0.1:5000/pipelines/1/trigger
```

### Delete a Pipeline

```bash
curl -X DELETE http://127.0.0.1:5000/pipelines/1
```
