from flask import Blueprint

chatbot_bp = Blueprint("chatbot_bp", __name__, template_folder="../templates")

from . import routes
