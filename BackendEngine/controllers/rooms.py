import logging
import settings
# import utils
import json

from flask import Blueprint, request, jsonify
from flask_cors import CORS, cross_origin
from usecases import rooms
# from usecases.booking_usecase import check_no_rooms
from datetime import datetime, timedelta
# from bson import json_util


room_controller = Blueprint("rooms", __name__)


@room_controller.route("/hi",methods=["GET"])
def hello():
    return jsonify({"Message":"Hi Webjini Rooms"})



# # ?done


@room_controller.route("/<token>", methods=["GET"])
def get_each_rooms(token):
    try:
        # print(token)
        room = rooms.get_each_rooms(token)  
        logging.info(f"Rooms retrieved successfully for token: {token}")
        return jsonify({"data": room,"Status":True})
    except Exception as e:
        # Handle exceptions and log the error
        logging.error(e)
        return jsonify({"error": "Internal server error","Status":False}), 500


# @room_controller.route("/get/room/website/<domain>", methods=["GET"])
# def get_rooms_domain_based(domain):
#     try:
#         # print(token)
#         rooms = room_usecase.get_domain_based_rooms(domain)
#         logging.info(f"Rooms retrieved successfully for token: {domain}")
#         return jsonify({"data": rooms,"Status":True})
#     except Exception as e:
#         # Handle exceptions and log the error
#         logging.error(e)
#         return jsonify({"error": "Internal server error","Status":False}), 500


@room_controller.route("/<token>/<hId>", methods=["GET"])
def get_all_rooms(token, hId):
    try:
        # print(token)
        room = rooms.get_all_rooms(token, hId)
        logging.info(f"Rooms retrieved successfully for token: {token}")
        return jsonify({"data": room,"Status":True})
    except Exception as e:
        # Handle exceptions and log the error
        logging.error(e)
        return jsonify({"error": "Internal server error","Status":False}), 500

# # ?done


@room_controller.route("/create/<token>", methods=["POST"])
def create_room(token):
    try:
        room_details = request.get_json(force=True)
        status, message = rooms.add_room(room_details, token)
        logging.info(f"Room created successfully with token: {token}")
        return jsonify({"status": status, "message": message})
    except Exception as ex:
        logging.error(ex)
        return jsonify({"status": "error", "message": message}), 500

# # ?done


@room_controller.route("/delete/<roomtype>", methods=["POST"])
def delete_room(roomtype):
    try:
        room_details = request.get_json(force=True)
        token = room_details.get("token")
        hId = room_details.get("hId")
        status, message = rooms.delete_room(roomtype, token, hId)
        logging.info(f" deleted successfully. Status: {status}, Message: {message}")
        return jsonify({"status": status, "message": message})
    except Exception as ex:
        logging.error(ex)
        return jsonify({"status": "error", "message": message}), 500
# ?done


@room_controller.route("/edit/<token>", methods=["POST"])
def edit_room(token):
    try:
        room_details = request.get_json(force=True)
        status, message = rooms.edit_room_db(room_details, token)
        logging.info(f" Status: {status}, Message: {message}")
        return jsonify({"status": status, "message": message})
    except Exception as ex:
        logging.error(ex)
        return jsonify({"status": "error", "error": "Internal server error"}), 500


# API for  Rooms and prices dynamic
@room_controller.route("/engine/<id>", methods=["POST"])
def get_all_rooms_engine(id):
    try:
        room_details = request.get_json(force=True)
        room, prices = rooms.get_all_rooms_engine_with_price(room_details, id)
        # print(rooms)
        logging.info(f"{id}. Details: {room}, Prices: {prices}")
        return jsonify({"Status": True, "Details": room, "Price": prices})
    except Exception as ex:
        logging.error(f"{ex}")
        return jsonify({"Status": False, "Message": str(ex)}), 500


# API for avaiblity of rooms
@room_controller.route("/availablity", methods=["POST"])
def get_availablity_booking():
    try:
        booking_data = request.get_json(force=True)
        logging.info(f"{booking_data}")
        status, message = rooms.check_list_of_rooms_available_daterange(booking_data)
        logging.info(f"{status},{message}")
        return jsonify({"status": status, "Avaiblity": message})
    except Exception as ex:
        logging.info(f"{ex}")
        return ({"Status": False, "Message": "{}".format(ex)}), 500