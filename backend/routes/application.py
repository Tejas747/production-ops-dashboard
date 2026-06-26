from flask import Blueprint, jsonify
from mock_data.application import get_application_data

application_bp = Blueprint("application", __name__)

@application_bp.route("/api/application")
def application():
    return jsonify(get_application_data())