from models.country import Country

class GuestInfo:
    def __init__(self, guestName, emailId, phone):
        self.guestName = guestName
        self.emailId = emailId
        self.phone = phone
       

    def to_dict(GuestInfo):
        return {
            "guestName": GuestInfo.guestName,
            "EmailId": GuestInfo.emailId,
            "Phone": GuestInfo.phone,
            
        }

    def from_dict(guestInfo_dict):
        return GuestInfo(
            guestName=guestInfo_dict.get("guestName"),
            emailId=guestInfo_dict.get("EmailId"),
            phone=guestInfo_dict.get("Phone"),  
        )