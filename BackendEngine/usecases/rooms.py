import utils
import constants
import pymongo
import json
import settings
import logging
from bson import json_util
from usecases import booking
from datetime import datetime, date, timedelta
from models.Room import Room
from models.roomFacilities import RoomFacility

logging.basicConfig(format=settings.LOG_FORMATTER)
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(settings.LOG_LEVEL)
client = pymongo.MongoClient(settings.DBURL)
db = client[settings.DBNAME]

def add_roomnumber_in_createprocess(n,start):
    number_list = [str(int(start) + i) for i in range(n)]
    return number_list

# #?DONE
def add_room(room_details, token):
    # try:
        logging.info(f"{room_details},{token}")
        room=Room.from_dict(room_details)
        jiniid = utils.Decode_jwt(token)
        ndid = jiniid.get("user")
        room.jiniId = ndid
        room_type = room.roomType
        hId = room_details.get("hId", "")
        room.ndid=ndid
        number = room_type+"01"

        room.roomNumbers = add_roomnumber_in_createprocess(int(room.noOfRooms),int(number))
        available_room = get_room(ndid, hId, room_type)
        if available_room:
            logging.info(f"False")
            return False, "Room already exist with the provided Room Type"
        room.roomTypeName=room_type
        db.Webjini_rooms.insert_one(Room.to_dict(room))
        
        logging.info(f"True")
        return True, "Success"
    # except Exception as ex:
    #     logging.error(f"{ex}")
    #     LOGGER.error("Unabel to create room error:{}".format(ex))
    #     return False, "Error Occured"

# #?NOT REQUIRED
def delete_room_db(ndid, hId, room_type_name):
    try:
        return db.Webjini_rooms.find_one_and_delete({"jiniId": ndid, "hId": hId, "roomType": room_type_name})
    except Exception as e:
        logging.error(f"Error in deleting room from db {e}")

# #?NOT REQUIRED
def delete_room(roomtype, token, hId):
    try:
        logging.info(f"{roomtype},{token}")
        ndid = utils.Decode_jwt(token)
        jiniid = ndid.get("user")
        available_room = delete_room_db(jiniid, hId, roomtype)
        logging.info(f"Room Deleted")
        return True, "Room Deleted"
    except Exception as ex:
        logging.error(f"{ex}")
        LOGGER.error("Unable to delete room error:{}".format(ex))
        return False, "Error Occured"

# #?DONE
def edit_room_db(room_details, token):
    try:
        logging.info(f"{room_details},{token}")
        
        ndid = utils.Decode_jwt(token)
        jiniId = ndid.get("user")
        room_type = room_details.get("roomType", "1")
        hId = room_details.get("hId")
        room_exist=get_room(jiniId,hId,room_type)
        number = room_type+"01"
        if room_exist:
            room=Room.from_dict(room_exist)
            room.roomName=room_details.get("roomName", "")
            room.roomDescription= room_details.get("roomDescription", "")
            room.child = room_details.get("child", -1)
            room.adult = room_details.get("adult", -1)
            room.noOfRooms = room_details.get("noOfRooms", 1)
            room.price= room_details.get("price", 0)
            room.roomImage= room_details.get("roomImage", [])
            facilities = room_details.get("roomFacilities", {})
            room.roomSubheading = room_details.get("roomSubheading", "enjoy")
            filter_criteria = {
                "jiniId": jiniId,
                "hId": hId,
                "roomType": room_type
            }
            room.roomFacilities=RoomFacility.from_dict(facilities)
            room_updated=room.to_dict()
            result = db.Webjini_rooms.update_one(filter_criteria, {"$set": room_updated})
            if result.modified_count > 0:
                logging.info(f"Room Updated")
                return True, "Room Updated"
            else:
                logging.info(f"No Matching")
                return False, "No matching room found for update"
        else:
            return False, "Room not found or not updated"
    except Exception as ex:
        logging.info(f"{ex}")
        LOGGER.error("Unablr to edit room error:{}".format(ex))
        return False, "Error Occured"

# #?NOT DONE
def get_room(ndid, hId, room_type):
    try:
        return db.Webjini_rooms.find_one({"jiniId": ndid, "hId": hId, "roomType": room_type})
    except Exception as ex:
        logging.error(ex)
        return None

def get_each_rooms(token):
    try:
        data = utils.Decode_jwt(token)
        rooms = db.Webjini_rooms.find({"jiniId": data.get("user")})
        room = []
        for i in rooms:
            room.append(i)
        return json.loads(json_util.dumps(room))
    except Exception as ex:
        logging.error(ex)
        return None
    
# def get_domain_based_rooms(domain):
#     try:
#         profile = db.Zucks_profile.find_one({"domain":domain})
#         rooms = db.Rooms.find({"ndid": profile.get("uId")})
#         return json.loads(json_util.dumps(rooms))
#     except Exception as ex:
#         logging.error(ex)
#         return None



# #?NOT DONE
def get_all_rooms(token, hId):
    try:
        data = utils.Decode_jwt(token)
        rooms = db.Webjini_rooms.find({"jiniId": data.get("user"), "hId": hId})
        room = []
        for i in rooms:
            room.append(i)
        return json.loads(json_util.dumps(room))
    except Exception as ex:
        logging.error(ex)
        return None

# #?NOT DONE
# def get_all_rooms_engine(ndid, hId):
#     try:
#         logging.info(f"{ndid}")
#         rooms = db.Rooms.find({"ndid": ndid, "hId": hId})
#         logging.info(f"{rooms}")
#         return json.loads(json_util.dumps(rooms))
#     except Exception as ex:
#         logging.error(ex)
#         return None

# #?NOT DONE
# def room_getBookingCount_on_date(token, hId, checkin):
#     try:
#         logging.info(f"{token},{checkin}")
#         Delux = SuperDelux = Suite = Premium = 0

#         ndid = utils.get_ndid(token)
#         query = {
#             "hId": hId,
#             "ndid": ndid,
#             "checkIn": {
#                 "$lte": checkin
#             },
#             "checkOut": {
#                 "$gt": checkin
#             }
#         }
#         bookings = db.Bookings.find(query)

#         for booking in bookings:
#             for bookingdata in booking.get("Bookings"):
#                 if bookingdata.get("Qty") > 0:
#                     if bookingdata.get('RoomType') == "1":
#                         Delux += bookingdata.get("Qty")

#                     if bookingdata.get('RoomType') == "2":
#                         SuperDelux += bookingdata.get("Qty")

#                     if bookingdata.get('RoomType') == "3":
#                         Suite += bookingdata.get("Qty")

#                     if bookingdata.get('RoomType') == "4":
#                         Premium += bookingdata.get("Qty")
#         logging.info(f"{Delux},{SuperDelux},{Suite},{Premium}")
#         return Delux, SuperDelux, Suite, Premium
#     except Exception as ex:
#         logging.error(ex)
#         return None



# #?NOT DONE
def get_all_rooms_prices(room_details, ndid, hId):
    try:
        logging.info(f"{room_details},{ndid}")
        price = {}
        rooms = db.Webjini_rooms.find({"jiniId": ndid, "hId": hId})
        for room in rooms:
            booking_details = {
                "checkIn": room_details.get('checkIn'),
                "checkOut": room_details.get('checkOut'),
                "roomType": room.get('roomType')
            }
            amount = booking.calculate_booking_total(
                booking_details, ndid, hId)
            price[room.get('roomType')] = amount
        logging.info(f"{price}")
        return price
    except Exception as ex:
        logging.error(ex)
        return None

#?NOT DONE
def get_all_rooms_engine_with_price(room_details, ndid):
    try:
        logging.info(f"{room_details},{ndid}")
        hId = room_details.get("hId")
        rooms = db.Webjini_rooms.find({"jiniId": ndid, "hId": hId})
        prices = get_all_rooms_prices(room_details, ndid, hId)
        logging.info(f"{rooms},{prices}")
        return json.loads(json_util.dumps(rooms)), prices
    except Exception as ex:
        logging.error(ex)
        return None
# # =========================================PRICES===================================================

# #?NOT REQUIRED
# def get_id(booking_count):
#     try:
#         logging.info(f"{booking_count}")
#         for i in range(5 - len(booking_count)):
#             booking_count = "0" + booking_count
#         logging.info(f"{booking_count}")
#         return booking_count
#     except Exception as ex:
#         logging.error(ex)
#         return None

# #?NOT REQUIRED
def get_next_dates_from_date(date, number):
    try:
        current_date = datetime.strptime(date, "%Y-%m-%d").date()
        dates = []
        for i in range(0, number):
            next_n_days = current_date + timedelta(days=i)
            dates.append(next_n_days)

        return dates
    except Exception as ex:
        logging.error(f"{ex}")
        return None
# # 6

# #?NOT REQUIRED
def get_prev_dates_from_date(date, number):
    try:
        current_date = datetime.strptime(date, "%Y-%m-%d").date()
        dates = []
        for i in range(number, 0, -1):
            next_n_days = current_date - timedelta(days=i)
            dates.append(next_n_days)

        return dates
    except Exception as ex:
        logging.error(f"{ex}")
        return None
    
# #?NOT REQUIRED
# def return_weakday(date):
#     try:
#         date = datetime.strptime(date, '%Y-%m-%d').date()

#         day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

#         # Get the day name using the day_of_week as an index
#         day_name = day_names[date.weekday()]
#         return day_name
#     except Exception as ex:
#         logging.error(ex)
#         return None


def get_dates_in_range(start_date, end_date):
    try:
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        # Calculate the number of days between start_date and end_date
        delta = end_date - start_date
        # Generate a list of dates within the date range
        date_list = [start_date + timedelta(days=i) for i in range(delta.days)]
        return date_list
    except Exception as e:
        logging.error(f"Error in getting date in range:{e}")



def check_list_of_rooms_available_daterange(booking_details):
    try:
        ndid = booking_details.get("ndid")
        hId = booking_details.get("hId")
        checkin = booking_details.get("checkin")
        checkout = booking_details.get("checkout")
        number_of_days_between = get_dates_in_range(checkin, checkout)
        # print(number_of_days_between)
        available = {}
        rooms = db.Webjini_rooms.find({"jiniId": ndid, "hId": hId})
        for room in rooms:
            min_room = 99999
            inventory = room.get('inventoryStatus', {})
            for days in number_of_days_between:
                if (str(days) in inventory):
                    max_room = int(inventory[str(days)])
                else:
                    max_room = int(room.get('noOfRooms'))
                if (max_room < min_room):
                    min_room = max_room
            
            available[room.get("roomType")] = min_room
             
        return True, available
    except:
        return False, available