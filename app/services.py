from flask import jsonify
from .models import CommandType, pipelines


def create_pipeline(data):
    for stage in data.get("stages", []):
        if not CommandType.is_valid(stage.get("type")):
            return jsonify({"error": f"Invalid command type: {stage.get('type')}"}), 400
    pipeline_id = len(pipelines) + 1
    pipelines[pipeline_id] = data
    return jsonify({"id": pipeline_id}), 201


def get_pipeline(pipeline_id):
    pipeline = pipelines.get(pipeline_id)
    if not pipeline:
        return jsonify({"error": "Pipeline not found"}), 404
    return jsonify(pipeline)


def update_pipeline(pipeline_id, data):
    if pipeline_id not in pipelines:
        return jsonify({"error": "Pipeline not found"}), 404
    pipelines[pipeline_id] = data
    return jsonify({"message": "Pipeline updated"})


def delete_pipeline(pipeline_id):
    if pipeline_id not in pipelines:
        return jsonify({"error": "Pipeline not found"}), 404
    del pipelines[pipeline_id]
    return jsonify({"message": "Pipeline deleted"})


def trigger_pipeline(pipeline_id):
    pipeline = pipelines.get(pipeline_id)
    if not pipeline:
        return jsonify({"error": "Pipeline not found"}), 404

    for stage in pipeline.get("stages", []):
        if stage["type"] == CommandType.RUN:
            print(f"Running command: {stage['command']}")
        elif stage["type"] == CommandType.BUILD:
            print(f"Building Docker image from: {stage['dockerfile']}")
            # Simulate Docker build and push to ECR
            print(
                f"Successfully built and pushed Docker image from {stage['dockerfile']} to ECR"
            )
        elif stage["type"] == CommandType.DEPLOY:
            print(f"Deploying Kubernetes manifest: {stage['manifest']}")
            # Simulate kubectl apply
            print(
                f"Successfully applied Kubernetes manifest {stage['manifest']} to the cluster"
            )
        else:
            return jsonify({"error": f"Unknown command type: {stage['type']}"}), 400

    return jsonify({"message": "Pipeline triggered"})
