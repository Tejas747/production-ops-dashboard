from flask import Blueprint, jsonify, request

ai_bp = Blueprint("ai", __name__)

@ai_bp.route("/api/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "")
    return jsonify({
        "question": question,
        "answer": "AI assistant coming in Phase 6."
    })