from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging
import smtplib
import base64
import ast
from email.message import EmailMessage
from email.mime.text import MIMEText
from datetime import datetime

def send_email(subject, body, sender,password, recipients):
    try:
        # Create a MIME message
        msg = MIMEText(body,'html')
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = ', '.join(recipients)
        # Attach the HTML body
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, recipients, msg.as_string())
        smtp_server.quit()
    except Exception as ex:
        logging.error(f"{ex}")
        return None, "{}".format(ex)


def Send_Query_recieved_to_client(CompanyName,Name,user_email,user_subject,user_description,user_phone,user_country,user_address,client_email,client_main_mail,client_main_pass):
    try:
        name = Name if Name else user_email
        Subject = "Query Received from "+name
        email_list = client_email.split(',')
        To = email_list
        From = client_main_mail
        password = client_main_pass
        body = '''
            <!DOCTYPE html>
            <html>
                <body>
                    <div style="padding:20px 0px">
                        <p> Dear {}, </p>
                        <p> We have received a query from your website.</p>
                        <p>Please reply to the user for their query</p>
                        <p>Customer Name - {}</p>
                        <p>Customer EmailId - {}</p>
                        <p>Customer Number - {}</p>
                        <p>Country- {}</p>
                        <p>Subject - {}</p>
                        <p>Description - {}</p>
                    </div>
                </body>
            </html>
        '''.format(CompanyName,Name,user_email,user_phone,user_country,user_subject,user_description)
        send_email(subject=Subject, body=body, sender=From, recipients=To,password=password)
    except Exception as ex:
        logging.error(f"{ex}")
        return None, "{}".format(ex)