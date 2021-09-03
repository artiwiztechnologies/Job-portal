from db import db
import datetime
import requests

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    phonenumber = db.Column(db.String(80))
    photoURL = db.Column(db.String(100))
    email = db.Column(db.String(200))
    password = db.Column(db.String(80))
    active = db.Column(db.Boolean())
    address = db.Column(db.String())
    subscription_id = db.Column(db.String())
    expiry_date =  db.Column(db.String())
    created_date = db.Column(db.String())
    status  = db.Column(db.Integer ) #not verified is 1 and 2 is verified and 3 is admin
    dateTime = db.Column(db.DateTime, default=datetime.datetime.now())
    token = db.Column(db.String())
    # tempotp  = db.Column(db.Integer ) 


    def __init__(self, email, password, phonenumber, name, photoURL, address, active, status ):
        self.email = email
        self.password = password
        self.status = status
        self.phonenumber = phonenumber
        # self.tempotp = tempotp
        self.name = name
        self.photoURL = photoURL
        self.address = address
        self.active = active


    def json(self):
        return {
            'id': self.id,
            'email': self.email,
            'phonenumber': self.phonenumber,
            'name': self.name,
            'photoURL': self.photoURL,
            'address': self.address,
            'status': self.status
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    # def send_otp(self):
    #     requests.get("http://trans.smsfresh.co/api/sendmsg.php?user=hkartthik97&pass=123456&sender=ARTOTP&phone={}&text=Your verfication code is:{} Dont share this code with anyone.&priority=ndnd&stype=normal".format(self.phonenumber,self.tempotp))

    def send_verification_email(self, id, receiver_email, token):

        print("mail")

        sender_email = "t8910ech@gmail.com"
        password = "8910@tech"
        # receiver_email = receiver_email

        message = MIMEMultipart("alternative")
        message["Subject"] = "multipart test"
        message["From"] = sender_email
        message["To"] = receiver_email

        text = """\
        Hi,
        How are you?
        Real Python has many great tutorials:
        www.realpython.com"""
        html = """\
        <html>
        <body>
            <p>Hi,<br>
            Click 
            <a href="http://127.0.0.1:5005/confirm-email/{}/{}" text-decoration="none"> here</a> 
             to verify.
            </p>
        </body>
        </html>
        """.format(id, token)
        # print("http://127.0.0.1:5005/confirm-email/", token)

        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part1)
        message.attach(part2)

        # Create secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )

    @classmethod
    def find_by_username(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_phonenumber(cls, phonenumber):
        return cls.query.filter_by(phonenumber=phonenumber).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

