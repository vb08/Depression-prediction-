from flask import render_template, request, jsonify
from . import chatbot_bp

# Chatbot page
@chatbot_bp.route("/chatbot")
def chatbot_page():
    return render_template("chatbot.html")

# Chatbot API endpoint
@chatbot_bp.route("/chatbot_api", methods=["POST"])
def chatbot_api():
    user_msg = request.json.get("message", "").lower()
    if "hello" in user_msg or "hi" in user_msg:
        return jsonify({"response": "Hello! I'm here to help 💛 How are you feeling today?"})
    if "sad" in user_msg:
        return jsonify({"response": "I'm sorry you're feeling sad 💛 I'm here to listen."})
    if "stress" in user_msg:
        return jsonify({"response": "Stress is difficult. Try deep breathing for 2 minutes."})
    if "depression" in user_msg:
        return jsonify({"response": "Depression is serious. Talking to someone helps a lot 💛"})
    return jsonify({"response": "I’m here for you. Tell me more."})
