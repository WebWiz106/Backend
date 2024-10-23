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


def verify_bot(data):
    apikey = data.get("apikey")
    user = db1.UserAccount.find_one({'user_key':apikey})
    if user and user['isHavingBot']:
        return True
    else:
        return False



def initiate_chat_session(data):
    apikey = data.get("apikey")
    sessionid = "user_" + str(utils.createChatSessionID())
    sessionid2 = "admin_" + str(utils.createChatSessionID())
    fetch_user = db1.UserAccount.find_one({'user_key':apikey})
    if fetch_user:
        initial_message = data.get('message')

        db1.LiveChatQuery.insert_one({
            "user_key":apikey,
            "user_sessionid":sessionid,
            "admin_sessionid":sessionid2,
            "message":initial_message,
            "startdate":str(datetime.now()),
            "closedat":"",
            "magicalLink":"https://bot.webjini.in/admin"+sessionid2+"?id=admin",
            "messageList":[{"sender":"user","message":initial_message,"sendat":str(datetime.now())}],
            "isClosed":False
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
        fetch_session = db1.LiveChatQuery.find_one({"user_sessionid":sessionid})
        if fetch_session:
            messsages=fetch_session['messageList']
            messsages.append({"sender":"user","message":message,"sendat":str(datetime.now())})
            db1.LiveChatQuery.find_one_and_update({"sessionid":sessionid},{"$set":{
                "messageList":messsages
            }})

            return True, "Sent",messsages
        else:
            return False, "Session Not Found",[]
    else:
        return False, "Account Not Found",[]
    

def send_reply_to_user(data):
    sessionid = data.get("sessionid")
    message = data.get("message")
    apikey = data.get("apikey")
    fetch_user = db1.UserAccount.find_one({'user_key':apikey})
    if fetch_user:
        fetch_session = db1.LiveChatQuery.find_one({"admin_sessionid":sessionid})
        if fetch_session:
            messsages=fetch_session['messageList']
            messsages.append({"sender":"admin","message":message,"sendat":str(datetime.now())})
            db1.LiveChatQuery.find_one_and_update({"sessionid":sessionid},{"$set":{
                "messageList":messsages
            }})
            return True, "Sent", messsages
        else:
            return False, "Session Not Found", []
        
    else:
        return False, "User not found", []
    

def get_session_messages(sessionid):
    fetch_session = db1.LiveChatQuery.find_one({"admin_sessionid":sessionid})
    if fetch_session:
        return fetch_session['messageList']
    
    fetch_session = db1.LiveChatQuery.find_one({"user_sessionid":sessionid})
    if fetch_session:
        return fetch_session['messageList']
    
    return []