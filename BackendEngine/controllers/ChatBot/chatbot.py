from flask import Blueprint , jsonify , request
from flask_cors import CORS,cross_origin
import utils
import json
import pymongo
import settings
from bson import json_util
from usecases import auth
from usecases.ChatBot import chat
from flasgger import swag_from

chatbot_controller = Blueprint('chatbot', __name__)

@chatbot_controller.route("/hi")
def hello():
    return {"Message":"Hi Chat System"}

#?Admin and client session id will be different so as client can not open admin interface and admin can not open client interface
#*API will hit to verify the API key and authenticate weather valid bot or not and also it will give details of company and logo
#1: API key get verified and bot is opened or closed
@chatbot_controller.route("/verify-bot",methods=["POST"])
def verify_chat_bot():
    data = request.get_json(force=True)
    status = chat.verify_bot(data)
    return jsonify({"status": status}),200

#2: Session created and bot opened
@chatbot_controller.route("/open-session",methods=["POST"])
def create_new_session():
    data = request.get_json(force=True)
    status = chat.initiate_chat_session(data)
    return jsonify({"status": status}),200


#API will hit to send session message to chat and user will be able to see chat soo give response of chat too.
@chatbot_controller.route("/message-in-session",methods=["POST"])
def send_message_in_session():
    data = request.get_json(force=True)
    status, message, conversation = chat.user_message_in_chat(data)
    return jsonify({"status": status, "message": message,"conversation":conversation}),200


@chatbot_controller.route("/reply-in-session",methods=["POST"])
def reply_message_in_session():
    data = request.get_json(force=True)
    status, message, conversation = chat.send_reply_to_user(data)
    return jsonify({"status": True, "message": "Message Sent","conversation":conversation}),200


@chatbot_controller.route("/close-session",methods=["POST"])
def close_existing_session():
    return jsonify({"status": True, "message": "Session Closed"}),200


#Create API to identify session and return chats
#Create a get api which return current chat based on session id
# @chatbot_controller.route("/<sessionid>",methods=["GET"])
# @swag_from({
#     'responses': {
#         200: {
#             'description': 'List of rooms',
#             'examples': {
#                 'application/json': {"status": True, "conversation":[
#                     {"sender":"user","message":"Hi","sendat":"2024-09-25 03:51:02.991868"},
#                     {"sender":"admin","message":"Hi","sendat":"2024-09-25 03:51:02.991868"},
#                     ]}
#             }
#         }
#     }
# })
def verifysession_showchat(sessionid):
    message = chat.get_session_messages(sessionid)
    return jsonify({"status": True, "conversation": message}),200


