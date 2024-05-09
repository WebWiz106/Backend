from models.guest_info import GuestInfo
from models.price import Price
from models.booking_item import BookingItem
from models.payment import Payment
from models.bookingmealplan import BookingMealPlan
from models.bookingpackages import BookingPackage
from models.promocode import PromoCode


class Bookings:
    def __init__(self, hId, jiniId, packages, promocode, mealPlan, bookingId, guestInfo, adult, kid, bookingItems, payment, checkIn, checkOut, price, bookingDate,roomNumbers, isCheckedIn=False, isCheckedOut=False):
        self.hId = hId
        self.roomNumbers=roomNumbers
        self.jiniId = jiniId
        self.bookingId = bookingId
        self.guestInfo = guestInfo
        self.adult = adult
        self.kid = kid
        self.bookingItems = bookingItems
        self.payment = payment
        self.promocode = promocode
        self.mealPlan = mealPlan
        self.packages = packages
        self.checkIn = checkIn
        self.checkOut = checkOut
        self.price = price
        self.bookingDate = bookingDate
        self.isCheckedIn = isCheckedIn == "true"
        self.isCheckedOut = isCheckedOut == "true"

    def to_dict(Bookings):
        return {
            "roomNumbers":Bookings.roomNumbers,
            "hId": Bookings.hId,
            "jiniId": Bookings.jiniId,
            "bookingId": Bookings.bookingId,
            "guestInfo": GuestInfo.to_dict(Bookings.guestInfo),
            "Adults": Bookings.adult,
            "Kids": Bookings.kid,
            "Bookings": [BookingItem.to_dict(item) for item in Bookings.bookingItems],
            "payment": Payment.to_dict(Bookings.payment),
            "promocode": PromoCode.to_dict(Bookings.promocode),
            "mealPlan": BookingMealPlan.to_dict(Bookings.mealPlan),
            "packages": BookingPackage.to_dict(Bookings.packages),
            "checkIn": Bookings.checkIn,
            "checkOut": Bookings.checkOut,
            "price": Price.to_dict(Bookings.price),
            "isCheckedIn": Bookings.isCheckedIn,
            "isCheckedOut": Bookings.isCheckedOut,
            "bookingDate": Bookings.bookingDate,
        }

    def from_dict(booking_dict):
        return Bookings(
            roomNumbers=booking_dict.get("roomNumbers",[]),
            hId=booking_dict.get("hId"),
            jiniId=booking_dict.get("jiniId"),
            bookingId=booking_dict.get("bookingId"),
            guestInfo=GuestInfo.from_dict(booking_dict.get("guestInfo")),
            adult=booking_dict.get("Adults"),
            kid=booking_dict.get("Kids"),
            bookingItems=[BookingItem.from_dict(
                item) for item in booking_dict.get("Bookings")],
            payment=Payment.from_dict(booking_dict.get("payment")),
            promocode=PromoCode.from_dict(booking_dict.get("promocode")),
            mealPlan=BookingMealPlan.from_dict(booking_dict.get("mealPlan")),
            packages=BookingPackage.from_dict(booking_dict.get("packages")),
            checkIn=booking_dict.get("checkIn"),
            checkOut=booking_dict.get("checkOut"),
            price=Price.from_dict(booking_dict.get("price")),
            isCheckedIn=booking_dict.get("isCheckedIn"),
            isCheckedOut=booking_dict.get("isCheckedOut"),
            bookingDate=booking_dict.get("bookingDate"),
        )
