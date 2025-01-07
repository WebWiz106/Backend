import jwt
import logging
import settings
import string
import pymongo
from datetime import datetime, timedelta
from random import *
# from usecases import user_usecase

logging.basicConfig(format=settings.LOG_FORMATTER)
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(settings.LOG_LEVEL)

client = pymongo.MongoClient(settings.DBURL)
client1 = pymongo.MongoClient(settings.DBURL1)
print("===========================Database============================")
db = client[settings.DBNAME]
db1 = client[settings.DBNAME1]

def create(data={}):
    # data contains email,password
    expiry_date = datetime.now() + timedelta(days=15)
    data["exp"] = expiry_date.timestamp()
    token = jwt.encode(data, settings.JWT_SECRETS, algorithm=settings.JWT_ALGORITHM)
    return token    


def Decode_jwt(token):
    data = jwt.decode(token, settings.JWT_SECRETS, algorithms=[settings.JWT_ALGORITHM])
    # This TOKEN have EMAIL AND PASSWORD of the user loggedin currently
    for i in data:
        if isinstance(data[i], str):
            data[i] = data[i]
        else:
            data[i] = data[i]

    # if "exp" in data and datetime.now().timestamp() > data["exp"]:
    #         raise ValueError("Token has expired")
    
    return data

def createAPIkey():
    characters = string.ascii_letters + string.digits + "!@#$%^&*()"
    api_key = ''.join(choice(characters) for _ in range(15))
    return api_key

def createMessageID():
    characters = string.ascii_letters + string.digits + "!@#$%^&*()"
    messageid = ''.join(choice(characters) for _ in range(20))
    return messageid

def createChatSessionID():
    characters = string.ascii_letters + string.digits + "!@#$%^&*()"
    messageid = ''.join(choice(characters) for _ in range(30))
    return messageid

def get_authenticated_user(token):
    data = Decode_jwt(token)
    user = data.get("user") or None

# def get_ndid(token):
#     try:
#         data = Decode_jwt(token)
#         user = user_usecase.get_user(data["Email"])
#         ndid = user.get("ndid")
#         return ndid
#     except Exception as ex:
#         raise ValueError("Unable to decode token error : {}", ex)


  
# def get_name(token):
#     try:
#         data = Decode_jwt(token)
#         user = user_usecase.get_user(data["Email"])
#         name = user.get("userName")
#         return name
#     except Exception as ex:
#         raise ValueError("Unable to decode token error : {}", ex)
    
# def get_email(token):
#     try:
#         data = Decode_jwt(token)
#         return data["Email"]
#     except Exception as ex:
#         raise ValueError("Unable to decode token error : {}", ex)


# def getdata(token):
    try:
        data = Decode_jwt(token)
        return data
    except Exception as ex:
        raise ValueError("Unable to decode token error : {}", ex)