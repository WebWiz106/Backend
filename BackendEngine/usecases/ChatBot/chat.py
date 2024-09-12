import pymongo
import json
import settings
import constants
import utils
import uuid
from models.bookings import Bookings

from datetime import datetime, date, timedelta
from usecases import rooms
from usecases.MailFire import basicmails
# from model.guest_info import GuestInfo
import logging

from utils import db1

def initiate_chat_session(data):
    sessionid = utils.createChatSessionID()
    apikey = data.get("apikey")
    fetch_user = db1.UserAccount.find_one({'user_key':apikey})
    if fetch_user:
        initial_message = data.get('message')

        db1.LiveChatQuery.insert_one({
            "user_key":apikey,
            "sessionid":sessionid,
            "message":initial_message,
            "startdate":str(datetime.now()),
            "closedat":"",
            "messageList":[]
        })

        return True
    else:
        return False


def user_message_in_chat(data):
    sessionid = data.get("sessionid")
    message = data.get("message")
    apikey = data.get("apikey")
    fetch_user = db1.UserAccount.find_one({'user_key':apikey})
    if fetch_user:
        fetch_session = db1.LiveChatQuery.find_one({"sessionid":sessionid})
        if fetch_session:
            messsages=fetch_session['messageList']
            messsages.append({"sender":"user","message":message,"sendat":str(datetime.now())})
            db1.LiveChatQuery.find_one_and_update({"sessionid":sessionid},{"$set":{
                "messageList":messsages
            }})
            return True, "Sent"
        else:
            return False, "Session Not Found"
    else:
        return False, "Account Not Found"
    

def send_reply_to_user(data):
    sessionid = data.get("sessionid")
    message = data.get("message")
    apikey = data.get("apikey")
    fetch_user = db1.UserAccount.find_one({'user_key':apikey})
    if fetch_user:
        fetch_session = db1.LiveChatQuery.find_one({"sessionid":sessionid})
        if fetch_session:
            messsages=fetch_session['messageList']
            messsages.append({"sender":"admin","message":message,"sendat":str(datetime.now())})
            db1.LiveChatQuery.find_one_and_update({"sessionid":sessionid},{"$set":{
                "messageList":messsages
            }})
            return True, "Sent"
        else:
            return False, "Session Not Found"
        
    else:
        return False, "User not found"