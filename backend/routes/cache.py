from flask import Blueprint, jsonify
from mock_data.cache import get_cache_data

cache_bp = Blueprint("cache", __name__)

@cache_bp.route("/api/cache")
def cache():
    return jsonify(get_cache_data())