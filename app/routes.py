from flask import Blueprint, request, jsonify
from .services import (
    create_pipeline,
    get_pipeline,
    update_pipeline,
    delete_pipeline,
    trigger_pipeline,
)

bp = Blueprint("routes", __name__)


@bp.route("/pipelines", methods=["POST"])
def create():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid input, expected JSON"}), 400
    return create_pipeline(data)


@bp.route("/pipelines/<int:id>", methods=["GET"])
def get(id):
    try:
        return get_pipeline(id)
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


@bp.route("/pipelines/<int:id>", methods=["PUT"])
def update(id):
    data = request.json
    if not data:
        return jsonify({"error": "Invalid input, expected JSON"}), 400
    return update_pipeline(id, data)


@bp.route("/pipelines/<int:id>", methods=["DELETE"])
def delete(id):
    try:
        return delete_pipeline(id)
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


@bp.route("/pipelines/<int:id>/trigger", methods=["POST"])
def trigger(id):
    try:
        return trigger_pipeline(id)
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500
