import logging
import settings

from flask import Flask
from flask_cors import CORS,cross_origin

from controllers.auth import auth_controller
from controllers.rooms import room_controller
from controllers.engine import booking_controller
from controllers.inventory import roominventory
from controllers.price import price_controller


logging.basicConfig(format=settings.LOG_FORMATTER)
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(settings.LOG_LEVEL)

app = Flask(__name__)
CORS(app)


app.register_blueprint(auth_controller,url_prefix="/auth")
app.register_blueprint(room_controller,url_prefix="/rooms")
app.register_blueprint(roominventory,url_prefix="/inventory")
app.register_blueprint(price_controller,url_prefix="/price")
app.register_blueprint(booking_controller,url_prefix="/bookings")


if __name__ == '__main__':
    app.config['DEBUG'] = settings.DEBUG
    app.run()