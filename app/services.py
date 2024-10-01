from flask import jsonify
from .models import CommandType, pipelines


def create_pipeline(data):
    if not isinstance(data, dict):
        return jsonify({"error": "Invalid input, expected JSON"}), 400
    if "stages" not in data or not isinstance(data["stages"], list):
        return (
            jsonify(
                {"error": "Invalid pipeline configuration, 'stages' must be a list"}
            ),
            400,
        )
    for stage in data.get("stages", []):
        if not CommandType.is_valid(stage.get("type")):
            return jsonify({"error": f"Invalid command type: {stage.get('type')}"}), 400
        if stage["type"] == CommandType.RUN and "command" not in stage:
            return jsonify({"error": "Missing 'command' for RUN stage"}), 400
        if stage["type"] == CommandType.BUILD and "dockerfile" not in stage:
            return jsonify({"error": "Missing 'dockerfile' for BUILD stage"}), 400
        if stage["type"] == CommandType.DEPLOY and "manifest" not in stage:
            return jsonify({"error": "Missing 'manifest' for DEPLOY stage"}), 400
    pipeline_id = len(pipelines) + 1
    pipelines[pipeline_id] = data
    return jsonify({"id": pipeline_id}), 201


def get_pipeline(pipeline_id):
    try:
        pipeline = pipelines.get(pipeline_id)
        if not pipeline:
            return jsonify({"error": "Pipeline not found"}), 404
        return jsonify(pipeline)
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


def update_pipeline(pipeline_id, data):
    if pipeline_id not in pipelines:
        return jsonify({"error": "Pipeline not found"}), 404
    if not isinstance(data, dict):
        return jsonify({"error": "Invalid input format, expected JSON"}), 400
    if "stages" not in data or not isinstance(data["stages"], list):
        return (
            jsonify(
                {"error": "Invalid pipeline configuration, 'stages' must be a list"}
            ),
            400,
        )
    for stage in data.get("stages", []):
        if not CommandType.is_valid(stage.get("type")):
            return jsonify({"error": f"Invalid command type: {stage.get('type')}"}), 400
        if stage["type"] == CommandType.RUN and "command" not in stage:
            return jsonify({"error": "Missing 'command' for RUN stage"}), 400
        if stage["type"] == CommandType.BUILD and "dockerfile" not in stage:
            return jsonify({"error": "Missing 'dockerfile' for BUILD stage"}), 400
        if stage["type"] == CommandType.DEPLOY and "manifest" not in stage:
            return jsonify({"error": "Missing 'manifest' for DEPLOY stage"}), 400
    pipelines[pipeline_id] = data
    return jsonify({"message": "Pipeline updated"})


def delete_pipeline(pipeline_id):
    try:
        if pipeline_id not in pipelines:
            return jsonify({"error": "Pipeline not found"}), 404
        del pipelines[pipeline_id]
        return jsonify({"message": "Pipeline deleted"})
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


def trigger_pipeline(pipeline_id):
    pipeline = pipelines.get(pipeline_id)
    if not pipeline:
        return jsonify({"error": "Pipeline not found"}), 404

    for stage in pipeline.get("stages", []):
        if stage["type"] == CommandType.RUN:
            if "command" not in stage:
                return jsonify({"error": "Missing 'command' for RUN stage"}), 400
            print(f"Running command: {stage['command']}")
        elif stage["type"] == CommandType.BUILD:
            if "dockerfile" not in stage:
                return jsonify({"error": "Missing 'dockerfile' for BUILD stage"}), 400
            print(f"Building Docker image from: {stage['dockerfile']}")
            # Simulate Docker build and push to ECR
            print(
                f"Successfully built and pushed Docker image from {stage['dockerfile']} to ECR"
            )
        elif stage["type"] == CommandType.DEPLOY:
            if "manifest" not in stage:
                return jsonify({"error": "Missing 'manifest' for DEPLOY stage"}), 400
            print(f"Deploying Kubernetes manifest: {stage['manifest']}")
            # Simulate kubectl apply
            print(
                f"Successfully applied Kubernetes manifest {stage['manifest']} to the cluster"
            )
        else:
            return jsonify({"error": f"Unknown command type: {stage['type']}"}), 400

    return jsonify({"message": "Pipeline triggered"})
