from flask import Blueprint , jsonify , request
from flask_cors import CORS,cross_origin
import utils
import json
import pymongo
import settings
from bson import json_util
from usecases import auth

auth_controller = Blueprint('auth', __name__)


from utils import db


@auth_controller.route("/hi")
def hello1():
    return {"Message":"Hi webjini"}


@auth_controller.route("/getuser/<token>",methods=["POST"])
def getUserWebjini(token):
    try:
        maintenance_details = request.get_json(force=True)
        ndid = utils.Decode_jwt(token)
        jiniId = ndid.get("user")
        email = maintenance_details.get("emailId")

        user,admin,access = auth.get_users_info(jiniId,email)
        profile = auth.get_users_profile(jiniId)
        websiteLink = auth.get_user_links(jiniId)

        return jsonify({"Status":True,
                        "Admin":admin, 
                        "userInfo":json.loads(json_util.dumps(user)),
                        "websiteLink":websiteLink,
                        "Profile":json.loads(json_util.dumps(profile)),
                        "Access":access})
    except:
        return jsonify({"Status":False})


@auth_controller.route("/createuser",methods=["POST"])
def createUser():
    try:
        maintenance_details = request.get_json(force=True)
        if(maintenance_details.get("register")=="true"):
            status,token,message = auth.register_user_webjini(maintenance_details)
            return jsonify({"Status":status,"Message":message,"Token":token})
        else:
            status,token,message= auth.login_user_webjini(maintenance_details)
            return jsonify({"Status":status,"Message":message,"Token":token})
    except:
        return jsonify({"Status":False})


@auth_controller.route("/edit/password",methods=["POST"])
def editUser_password():
    try:
        maintenance_details = request.get_json(force=True)
        status,message = auth.updatepassword_user(maintenance_details)
        return jsonify({"Status":status,"Message":message})
    except:
        return jsonify({"Status":False})

@auth_controller.route("/createprofile",methods=["POST"])
def createWebsitewebjini():
    try:
        maintenance_details = request.get_json(force=True)

        #=======Domain Generate==========
        domain = auth.randomDomainName(maintenance_details.get("hotelName"))
        locationid = auth.createHotelId()
        webjiniId = utils.Decode_jwt(maintenance_details.get("token"))
        
        #Check for website already exists with user
        try:
            isexists = db.Webjini_Profiles.find_one({"webjiniId":webjiniId.get("user")})
        except:
            isexists = None
        
        if isexists!=None:
            return jsonify(
                            {"Status":False,
                             "Message":"You have already created Profile with us.",
                        })

        else:
            website = "https://"+domain+".webjini.com"
            
            status = auth.create_profile(webjiniId.get("user"),locationid,maintenance_details,domain,website)
            return jsonify({"Status":status,"Message":"Profile Created Successfully"})
    except:
        return jsonify({"Status":False,"Message":"Website And Booking Engine Creation Failed"})
    

@auth_controller.route("/active/bookingengine",methods=["POST"])
def activateBookingEngine():
    try:
        maintenance_details = request.get_json(force=True)
        status,message = auth.activateBookingEngineTool(maintenance_details)
        return jsonify({"Status":status,"Message":message})
    except:
        return jsonify({"Status":False,"Message":"Something went wrong"})
    

@auth_controller.route("/deactive/bookingengine",methods=["POST"])
def deActivateBookingEngine():
    try:
        maintenance_details = request.get_json(force=True)
        status,message = auth.deactivateBookingEngineTool(maintenance_details)
        return jsonify({"Status":status,"Message":message})
    except:
        return jsonify({"Status":False,"Message":"Something went wrong"})


@auth_controller.route("/getuser/engine/<token>",methods=["GET"])
def FetchUserForEngineOnToken(token):
    try:
        Status,admin,user = auth.FetchUserForBookingAuth(token)
        return jsonify({"Status":Status,"Message":user,"isAdmin":admin})
    except:
        return jsonify({"Status":False,"User":"Some Problem Occurs"})



    