from flask import Blueprint, jsonify
from mock_data.infrastructure import get_infrastructure_data

infrastructure_bp = Blueprint("infrastructure", __name__)

@infrastructure_bp.route("/api/infrastructure")
def infrastructure():
    return jsonify(get_infrastructure_data())