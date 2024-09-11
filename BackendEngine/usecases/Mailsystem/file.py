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

def create_mail_account(data):
    creds = db1.WebjiniMailCreds.find_one({"type":"mail_cred"})
    user_name = data.get('name')
    company_name = data.get('company_name')
    user_email = data.get('email')
    user_key = utils.createAPIkey()
    account_type = data.get('account_type')
    from_email = data.get('from_email') if data.get('account_type')=="2" else creds['email']
    from_email_pass = data.get('from_email_pass') if data.get('account_type')=="2" else creds['password']

    fetch_user = db1.UserAccount.find_one({'user_email':user_email})
    if not fetch_user:
        db1.UserAccount.insert_one({
                "user_id":str(uuid.uuid4()),
                "domain":"",
                "company_name":company_name,
                "user_name":user_name,
                "user_email":user_email,
                "user_key":user_key,
                "account_type":account_type,
                "from_email":from_email,
                "from_email_pass":from_email_pass
        })
        return True,"Account Created",user_key
    else:
        return False,"User Exists","xxx"


def send_email_setup_function(data):
        mail_type = data.get("mail_type")
        api_code = data.get("apikey")

        fetch_user = db1.UserAccount.find_one({'user_key':api_code})
        if fetch_user:
            if mail_type=="contact":
                name = data.get('name',None)
                user_email = data.get('user_email',None)
                user_subject = data.get('user_subject',None)
                user_description = data.get('user_description',None)
                user_phone = data.get('user_phone',None)
                user_country = data.get('user_country',None)
                user_address = data.get('user_address',None)

                db1.UserContactQuery.insert_one({
                    "name":name,
                    "messageID":utils.createMessageID(),
                    "user_key":api_code,
                    "user_email":user_email,
                    "user_subject":user_subject,
                    "user_description":user_description,
                    "user_phone":user_phone,
                    "user_country":user_country,
                    "user_address":user_address,
                    "clientChats":[],
                    "clientreply":"",
                    "createdAt":str(datetime.now()),
                    "active":True
                })

                fetch_newsletter = db1.UserNewsletterQuery.find_one({"user_key":api_code,"user_email":user_email})
                if not fetch_newsletter:
                    db1.UserNewsletterQuery.insert_one({
                        "user_key":api_code,
                        "user_email":user_email
                    })


                #Mail Transfer to client
                basicmails.Send_Query_recieved_to_client(fetch_user['company_name'],name,user_email,user_subject,user_description,user_phone,user_country,user_address,fetch_user['user_email'],fetch_user['from_email'],fetch_user['from_email_pass'])
            
            if mail_type=="newsletter":
                user_email = data.get('user_email',None)
                fetch_newsletter = db1.UserNewsletterQuery.find_one({"user_key":api_code,"user_email":user_email})
                if not fetch_newsletter:
                    db1.UserNewsletterQuery.insert_one({
                        "user_key":api_code,
                        "user_email":user_email
                    })

            if mail_type=="ticket":
                pass
            
            if mail_type=="live_chat":
                pass

            if mail_type=="other":
                pass


            return True, "Query Created"

        else:
            return False, "Account Expired or not exists"
        

def user_contact_query_reply(data):
    queryid = data.get("queryid")
    api_code = data.get("apikey")
    message = data.get("message",None)
    fetch_user = db1.UserAccount.find_one({'user_key':api_code})
    if fetch_user:
        db1.UserContactQuery.find_one_and_update({'user_key':api_code,"messageID":queryid},{"$set": {
            "clientreply":message
        }})
        return True, "Message Sent"

        #Mail Fire from client to user
    else:
        return False, "Wrong Keys provided"