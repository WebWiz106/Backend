import json
import logging
from bson import json_util
from flask import Blueprint, request, jsonify
from flask_cors import CORS, cross_origin
from usecases import webjini_website


jini_controller = Blueprint('webjini_website', __name__)


@jini_controller.route("/hi")
def hello():
    return jsonify({"message": "hi webjini queries"})


@jini_controller.route("/create-query",methods=["POST"])
def QueryCreate():
    try:
        content = request.get_json(force=True)
        status = webjini_website.webjiniQueries(content)
        return jsonify({"Message":"Query Submitted","Status":status})
    except:
        return jsonify({"Message":"Some Problem Occured"})