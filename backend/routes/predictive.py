from flask import Blueprint, jsonify
from mock_data.predictive import get_predictive_data

predictive_bp = Blueprint("predictive", __name__)

@predictive_bp.route("/api/predictive")
def predictive():
    return jsonify(get_predictive_data())