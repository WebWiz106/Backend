import logging
import settings

from flask import Flask
from flask_cors import CORS,cross_origin
from flasgger import Swagger
from controllers.auth import auth_controller
from controllers.rooms import room_controller
from controllers.engine import booking_controller
from controllers.inventory import roominventory
from controllers.price import price_controller
from controllers.order import order_controller
from controllers.webjini_website import jini_controller

from controllers.Mailsystem.accountcreation import accountcreation_controller
from controllers.ChatBot.chatbot import chatbot_controller
from controllers.TicketMgmt.ticket import ticket_controller


logging.basicConfig(format=settings.LOG_FORMATTER)
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(settings.LOG_LEVEL)

app = Flask(__name__)
swagger = Swagger(app)
CORS(app)


app.register_blueprint(auth_controller,url_prefix="/auth")
app.register_blueprint(room_controller,url_prefix="/rooms")
app.register_blueprint(roominventory,url_prefix="/inventory")
app.register_blueprint(price_controller,url_prefix="/price")
app.register_blueprint(booking_controller,url_prefix="/bookings")
app.register_blueprint(order_controller,url_prefix="/order")
app.register_blueprint(jini_controller,url_prefix="/webjini")

#Booking engine
app.register_blueprint(accountcreation_controller,url_prefix="/mail")
app.register_blueprint(chatbot_controller,url_prefix="/chat-bot")
app.register_blueprint(ticket_controller,url_prefix="/ticket")

if __name__ == '__main__':
    app.config['DEBUG'] = settings.DEBUG
    app.run()