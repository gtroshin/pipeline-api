from flask import Blueprint, request, jsonify
from werkzeug.exceptions import BadRequest
from .services import (
    create_pipeline,
    get_pipeline,
    update_pipeline,
    delete_pipeline,
    trigger_pipeline,
)
from . import auth

bp = Blueprint("routes", __name__)


@bp.route("/pipelines", methods=["POST"])
@auth.login_required
def create():
    """
    Create a new pipeline.

    This endpoint expects a JSON payload with a 'stages' key containing a list of stages.
    Returns a 400 error if the input is invalid or a 500 error if an unexpected error occurs.
    """
    try:
        data = request.json
        if not data or "stages" not in data or not isinstance(data["stages"], list):
            return (
                jsonify(
                    {"error": "Invalid pipeline configuration, 'stages' must be a list"}
                ),
                400,
            )
        return create_pipeline(data)
    except BadRequest:
        return jsonify({"error": "Invalid input, expected JSON"}), 400
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


@bp.route("/pipelines/<int:id>", methods=["GET"])
@auth.login_required
def get(id):
    """
    Retrieve the configuration of an existing pipeline by ID.

    Args:
        id (int): The ID of the pipeline to retrieve.

    Returns:
        Response: A JSON response containing the pipeline configuration if found,
                  or an error message.
    """
    try:
        return get_pipeline(id)
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


@bp.route("/pipelines/<int:id>", methods=["PUT"])
@auth.login_required
def update(id):
    """
    Update an existing pipeline configuration.

    Args:
        id (int): The ID of the pipeline to update.

    Returns:
        Response: A JSON response indicating the result of the update operation
                    or an error.
    """
    data = request.json
    if not data:
        return jsonify({"error": "Invalid input, expected JSON"}), 400
    return update_pipeline(id, data)


@bp.route("/pipelines/<int:id>", methods=["DELETE"])
@auth.login_required
def delete(id):
    """
    Delete a pipeline configuration by ID.

    Args:
        id (int): The ID of the pipeline to delete.

    Returns:
        Response: A JSON response indicating the result of the delete operation
                    or an error.
    """
    try:
        return delete_pipeline(id)
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


@bp.route("/pipelines/<int:id>/trigger", methods=["POST"])
@auth.login_required
def trigger(id):
    """
    Trigger the execution of a pipeline by ID.

    Args:
        id (int): The ID of the pipeline to trigger.

    Returns:
        Response: A JSON response indicating the result of the trigger operation,
                  or an error.
    """
    try:
        return trigger_pipeline(id)
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500
