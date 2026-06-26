from flask import Blueprint, jsonify
from mock_data.infrastructure import get_infrastructure_data, get_dependency_graph

infrastructure_bp = Blueprint("infrastructure", __name__)

@infrastructure_bp.route("/api/infrastructure")
def infrastructure():
    return jsonify(get_infrastructure_data())

@infrastructure_bp.route("/api/dependency-graph")
def dependency_graph():
    return jsonify(get_dependency_graph())