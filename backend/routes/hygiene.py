from flask import Blueprint, jsonify
from mock_data.hygiene import get_hygiene_data

hygiene_bp = Blueprint("hygiene", __name__)

@hygiene_bp.route("/api/hygiene")
def hygiene():
    return jsonify(get_hygiene_data())