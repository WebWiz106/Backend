import razorpay
import settings
from flask import Blueprint, request, jsonify
from usecases import booking

order_controller = Blueprint('order', __name__)
import uuid  



@order_controller.route("/hi")
def hello():
    return jsonify({"Message":"Hello Payment !!"})


@order_controller.route("/create_order", methods=["POST"])
def create_order():
    try:
        data = request.get_json()
        amount = data.get('amount', 10000)  # Default to ₹100
        currency = data.get('currency', 'INR')
        print("DATA",data)
        amount=(float(amount))*100 

        hid = data.get("hId","")
        ndid = data.get("jiniId")

        type,apikey,secretkey = booking.getGateways(ndid,hid)
        print(type,apikey,secretkey)
        
        if type=="Razorpay":
            razorpay_client = razorpay.Client(auth=(apikey,secretkey))
            order = razorpay_client.order.create({
                'amount': amount,
                'currency': currency,
                'receipt': 'order_receipt_123',  # You can generate a unique receipt for each order
            })
            data["payment"]["RefNo"]=order['id']
            redirect_link=""
        else:
            order={}
            transaction_id,redirect_link = "",""
            data["payment"]["RefNo"]= transaction_id
            order["id"] = transaction_id
            
        print("into funt")
        status, message = booking.create_booking(data)
        # # print(message)
        # # Return the order ID to the client
        return jsonify({"Status":True,'order_id':order['id'],'redirectLink':redirect_link}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500



# @payment_controller.route("/getBookingDetailsforcancellation", methods=["POST"])
# def get_booking_details_for_cancellation():
#     try:
#         data = request.get_json()
#         bookingId = data.get('bookingId') 
#         hId = data.get("hId")
#         ndid = data.get("ndid")
#         status,data=booking_usecase.getBookingDetailForCancellation(ndid,hId,bookingId)
#         if status:
#             return jsonify({"status":status,"data":data})
#         return jsonify({"status":status})

#     except Exception as e:
#         return jsonify({'error': str(e)}), 500


# @payment_controller.route("/success/<ndid>/<hid>/<bookingId>/",methods=["GET"])
# def successPayment(ndid,hid,bookingId):
#     try:
#         status,data,logo,hotelname=booking_usecase.successPaymentGetData(ndid,hid,bookingId)

#         return render_template("success.html",data=data,logo=logo,hotelname=hotelname)
#     except Exception as ex:
#         return render_template("failure.html")