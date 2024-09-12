from flask import Blueprint , jsonify , request
from flask_cors import CORS,cross_origin
import utils
import json
import pymongo
import settings
from bson import json_util
from usecases import auth
from usecases.ChatBot import chat

chatbot_controller = Blueprint('chatbot', __name__)

@chatbot_controller.route("/hi")
def hello():
    return {"Message":"Hi Chat System"}


@chatbot_controller.route("/open-session",methods=["POST"])
def create_new_session():
    data = request.get_json(force=True)
    status = chat.initiate_chat_session(data)
    return jsonify({"status": status}),200


@chatbot_controller.route("/message-in-session",methods=["POST"])
def send_message_in_session():
    data = request.get_json(force=True)
    status, message = chat.user_message_in_chat(data)
    return jsonify({"status": status, "message": message}),200


@chatbot_controller.route("/reply-in-session",methods=["POST"])
def reply_message_in_session():
    data = request.get_json(force=True)
    status, message = chat.send_reply_to_user(data)
    return jsonify({"status": True, "message": "Message Sent"}),200


@chatbot_controller.route("/close-session",methods=["POST"])
def close_existing_session():
    return jsonify({"status": True, "message": "Session Closed"}),200

