from flask import Blueprint, jsonify
from mock_data.messaging import get_messaging_data

messaging_bp = Blueprint("messaging", __name__)

@messaging_bp.route("/api/messaging")
def messaging():
    return jsonify(get_messaging_data())