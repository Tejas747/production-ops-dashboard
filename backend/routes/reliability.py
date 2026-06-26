from flask import Blueprint, jsonify
from mock_data.reliability import get_reliability_data

reliability_bp = Blueprint("reliability", __name__)

@reliability_bp.route("/api/reliability")
def reliability():
    return jsonify(get_reliability_data())