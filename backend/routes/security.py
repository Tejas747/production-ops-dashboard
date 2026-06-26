from flask import Blueprint, jsonify
from mock_data.security import get_security_data

security_bp = Blueprint("security", __name__)

@security_bp.route("/api/security")
def security():
    return jsonify(get_security_data())