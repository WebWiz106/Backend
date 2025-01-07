from flask import Blueprint , jsonify , request
import utils
import requests

from utils import db

clarity_code_controller = Blueprint('clarity_code', __name__)

@clarity_code_controller.route("/hi")
def hello():
    return {"Message":"Hi clarity_code_controller"}


@clarity_code_controller.route("/get_clarity_data/<token>", methods=["GET"])
def get_clarity_data(token):
    try:
        data = utils.Decode_jwt(token)
        jiniId = data.get("user")
        profile = db.Webjini_Profiles.find_one({'webjiniId':jiniId})
        if profile.get('thirdPartyAccess').get('clarity_token'):

            num_of_days = request.args.get("numOfDays", "3")
            url = "https://www.clarity.ms/export-data/api/v1/project-live-insights"
            params = {
                "numOfDays": num_of_days
            }

            # Define headers
            headers = {
                "Content-Type": "application/json",
                "Authorization": str(profile.get('thirdPartyAccess').get('clarity_token'))
            }
            response = requests.get(url, headers=headers, params=params)
            return jsonify({"Status":True,"Data":response.json(), "Message":"Fetched Successfully"})
        else:
            return jsonify({"Status":False,"Data":{}, "Message":"Clarity Not enabled for client"})
    except:
        return jsonify({"Status":False,"Data":{}, "Message":"Something went wrong"})