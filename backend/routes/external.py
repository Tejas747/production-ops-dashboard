from flask import Blueprint, jsonify
from mock_data.external import get_external_data

external_bp = Blueprint("external", __name__)

@external_bp.route("/api/external")
def external():
    return jsonify(get_external_data())