from flask import Blueprint, jsonify
from mock_data.cost import get_cost_data

cost_bp = Blueprint("cost", __name__)

@cost_bp.route("/api/cost")
def cost():
    return jsonify(get_cost_data())