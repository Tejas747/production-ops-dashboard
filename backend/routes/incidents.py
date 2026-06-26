from flask import Blueprint, jsonify
from mock_data.incidents import get_incidents_data

incidents_bp = Blueprint("incidents", __name__)

@incidents_bp.route("/api/incidents")
def incidents():
    return jsonify(get_incidents_data())