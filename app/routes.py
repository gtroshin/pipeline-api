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
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Invalid input, expected JSON"}), 400
        return create_pipeline(data)
    except BadRequest:
        return jsonify({"error": "Invalid input, expected JSON"}), 400
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


@bp.route("/pipelines/<int:id>", methods=["GET"])
@auth.login_required
def get(id):
    try:
        return get_pipeline(id)
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


@bp.route("/pipelines/<int:id>", methods=["PUT"])
@auth.login_required
def update(id):
    data = request.json
    if not data:
        return jsonify({"error": "Invalid input, expected JSON"}), 400
    return update_pipeline(id, data)


@bp.route("/pipelines/<int:id>", methods=["DELETE"])
@auth.login_required
def delete(id):
    try:
        return delete_pipeline(id)
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


@bp.route("/pipelines/<int:id>/trigger", methods=["POST"])
@auth.login_required
def trigger(id):
    try:
        return trigger_pipeline(id)
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500
