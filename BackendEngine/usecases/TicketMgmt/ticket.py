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