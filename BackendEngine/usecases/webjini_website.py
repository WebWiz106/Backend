import datetime
import pymongo
import settings
import uuid
client = pymongo.MongoClient(settings.DBURL)
db = client[settings.DBNAME]

def webjiniQueries(content):
    try:
        Name = content.get("Name","")
        Email = content.get("Email","")
        Phone = content.get("Phone","")
        Message = content.get("Message","")
        Team = content.get("Team","")
        Subject = content.get("Subject","")

        count = db.Jini_Queries.count_documents({})
      
        
        db.Jini_Queries.insert_one({
            "ticketId":"Webjini-Ticket:"+str(count+1),
            "Name":Name,
            "Email":Email,
            "Phone":Phone,
            "Message":Message,
            "Team":Team,
            "Subject":Subject,
            "leadGeneratedOn":str(datetime.datetime.now().date()),
            "Remark":"",
            "openStatus":True
        })

        return True

    except:
        return False
   