from flask import Blueprint, jsonify
from mock_data.database import get_database_data

database_bp = Blueprint("database", __name__)

@database_bp.route("/api/database")
def database():
    return jsonify(get_database_data())