from flask import Blueprint , jsonify , request
from flask_cors import CORS,cross_origin
import utils
import json
import pymongo
import settings
from bson import json_util
from usecases import auth
from usecases.Mailsystem import file
from usecases.ChatBot import chat
from flasgger import swag_from

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
                "NEWSLETTER_API":"https://webjini.in/mail/send/data"
                # "TICKET_API":"https://webjini.in/mail/send/data",
                # "LIVE_CHAT_API":"https://webjini.in/mail/send/data",
                # "DATA_API":"https://webjini.in/mail/send/data"
            }})
        return jsonify({"status": status, "message": message})
    
    except Exception as ex:
        return jsonify({"status": "error"}), 500
    

#Create Mail for contact, newsletter
@accountcreation_controller.route("/send/data", methods=["POST"])
@swag_from({
    'summary': 'Send email to client',
    'description': 'API to send emails to clients based on different mail types such as contact, newsletter, etc.',
    'requestBody': {
        'required': True,
        'content': {
            'application/json': {
                'schema': {
                    'type': 'object',
                    'properties': {
                        'mail_type': {
                            'type': 'string',
                            'description': 'Type of mail to send (contact, newsletter, ticket, live_chat, other)',
                            'example': 'contact'
                        },
                        'apikey': {
                            'type': 'string',
                            'description': 'API key for authentication',
                            'example': 'abcdef123456'
                        },
                        'name': {
                            'type': 'string',
                            'description': 'Name of the user (required for contact type)',
                            'example': 'John Doe'
                        },
                        'user_email': {
                            'type': 'string',
                            'description': 'Email address of the user',
                            'example': 'johndoe@example.com'
                        },
                        'user_subject': {
                            'type': 'string',
                            'description': 'Subject of the user\'s message (required for contact type)',
                            'example': 'Support Request'
                        },
                        'user_description': {
                            'type': 'string',
                            'description': 'Description of the issue or query (required for contact type)',
                            'example': 'Issue with account login.'
                        },
                        'user_phone': {
                            'type': 'string',
                            'description': 'Phone number of the user',
                            'example': '+1234567890'
                        },
                        'user_country': {
                            'type': 'string',
                            'description': 'Country of the user',
                            'example': 'USA'
                        },
                        'user_address': {
                            'type': 'string',
                            'description': 'Address of the user',
                            'example': '123 Main St, Anytown, USA'
                        }
                    },
                    'required': ['mail_type', 'apikey']
                },
                'example': {
                    'mail_type': 'contact',
                    'apikey': 'abcdef123456',
                    'name': 'John Doe',
                    'user_email': 'johndoe@example.com',
                    'user_subject': 'Support Request',
                    'user_description': 'Issue with account login.',
                    'user_phone': '+1234567890',
                    'user_country': 'USA',
                    'user_address': '123 Main St, Anytown, USA'
                }
            }
        }
    },
    'responses': {
        200: {
            'description': 'Email sent successfully',
            'content': {
                'application/json': {
                    'examples': {
                        'success': {
                            'summary': 'Successful response',
                            'value': {
                                'status': True,
                                'message': 'Query Created'
                            }
                        }
                    }
                }
            }
        },
        400: {
            'description': 'Bad Request',
            'content': {
                'application/json': {
                    'examples': {
                        'missing_fields': {
                            'summary': 'Missing required fields',
                            'value': {
                                'status': False,
                                'message': 'Missing required fields'
                            }
                        }
                    }
                }
            }
        },
        500: {
            'description': 'Internal Server Error',
            'content': {
                'application/json': {
                    'examples': {
                        'error': {
                            'summary': 'Error response',
                            'value': {
                                'status': 'error',
                                'message': 'An error occurred while processing the request'
                            }
                        }
                    }
                }
            }
        }
    }
})
def sendMailtoClient():
    try:
        user_details = request.get_json(force=True)
        status, message = file.send_email_setup_function(user_details)
        return jsonify({"status": status, "message": message}), 200
    
    except Exception as ex:
        return jsonify({"status": "error", "message": str(ex)}), 500


#Reply for contact mail
@accountcreation_controller.route("/send/mail/reply", methods=["POST"])
def sendMailReplyfromClient():
    try:
        user_details = request.get_json(force=True)
        status, message = file.send_email_setup_function(user_details)
        return jsonify({"status": status, "message": message}),200
    
    except Exception as ex:
        return jsonify({"status": "error"}), 500