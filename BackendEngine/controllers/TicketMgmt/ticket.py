from flask import Blueprint , jsonify , request
from flask_cors import CORS,cross_origin
import utils
import json
import pymongo
import settings
from bson import json_util
from usecases import auth
from usecases.Mailsystem import file

ticket_controller = Blueprint('ticket', __name__)

@ticket_controller.route("/hi")
def hello():
    return {"Message":"Hi Ticket System"}



@ticket_controller.route("/open-ticket",methods=["POST"])
def create_new_ticket():
    return jsonify({"status": True, "message": "Ticket Created"}),200


@ticket_controller.route("/message-in-ticket",methods=["POST"])
def send_message_in_ticket():
    return jsonify({"status": True, "message": "Message Sent"}),200


@ticket_controller.route("/reply-in-ticket",methods=["POST"])
def reply_message_in_ticket():
    return jsonify({"status": True, "message": "Message Sent"}),200


@ticket_controller.route("/close-ticket",methods=["POST"])
def close_existing_ticket():
    return jsonify({"status": True, "message": "Ticket Closed"}),200