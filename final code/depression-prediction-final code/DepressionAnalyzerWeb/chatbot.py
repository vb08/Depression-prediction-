from flask import Blueprint, request, jsonify
import random

chatbot_bp = Blueprint('chatbot_bp', __name__)

responses = [
    "It's okay to feel low sometimes. Have you tried talking to someone you trust?",
    "Your feelings matter. Try taking a deep breath.",
    "Would you like a motivational quote?",
    "Healing takes time — and you're doing just fine.",
]

@chatbot_bp.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.form.get('message', '')
    reply = random.choice(responses)
    return jsonify({'response': reply})