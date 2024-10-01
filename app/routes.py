from flask import Blueprint, request
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
    return create_pipeline(data)


@bp.route("/pipelines/<int:id>", methods=["GET"])
def get(id):
    return get_pipeline(id)


@bp.route("/pipelines/<int:id>", methods=["PUT"])
def update(id):
    data = request.json
    return update_pipeline(id, data)


@bp.route("/pipelines/<int:id>", methods=["DELETE"])
def delete(id):
    return delete_pipeline(id)


@bp.route("/pipelines/<int:id>/trigger", methods=["POST"])
def trigger(id):
    return trigger_pipeline(id)
