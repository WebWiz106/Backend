from flask import Blueprint , jsonify , request
from flask_cors import CORS,cross_origin
import utils
import json
import pymongo
import settings
from bson import json_util
from usecases import auth
from usecases.Mailsystem import file

accountcreation_controller = Blueprint('accountcreation', __name__)

@accountcreation_controller.route("/hi")
def hello():
    return {"Message":"Hi Mail System"}


#Create Account
@accountcreation_controller.route("/create/account", methods=["POST"])
def createAccount():
    try:
        user_details = request.get_json(force=True)
        status, message,user_key = file.create_mail_account(user_details)
        if status:
            return jsonify({"status": status, "message": message,"details":{
                "API_KEY":user_key,
                "CONTACT_API":"https://webjini.in/mail/send/data",
                "NEWSLETTER_API":"https://webjini.in/mail/send/data",
                "TICKET_API":"https://webjini.in/mail/send/data",
                "LIVE_CHAT_API":"https://webjini.in/mail/send/data",
                "DATA_API":"https://webjini.in/mail/send/data"
            }})
        return jsonify({"status": status, "message": message})
    
    except Exception as ex:
        return jsonify({"status": "error"}), 500
    

#Create Mail for contact, newsletter
@accountcreation_controller.route("/send/data", methods=["POST"])
def sendMailtoClient():
    try:
        user_details = request.get_json(force=True)
        status, message = file.send_email_setup_function(user_details)
        return jsonify({"status": status, "message": message}),200
    
    except Exception as ex:
        return jsonify({"status": "error"}), 500

#Reply for contact mail
@accountcreation_controller.route("/send/mail/reply", methods=["POST"])
def sendMailReplyfromClient():
    try:
        user_details = request.get_json(force=True)
        status, message = file.send_email_setup_function(user_details)
        return jsonify({"status": status, "message": message}),200
    
    except Exception as ex:
        return jsonify({"status": "error"}), 500