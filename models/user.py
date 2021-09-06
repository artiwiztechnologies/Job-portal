from db import db
import datetime
import requests
from flask import Flask, request, url_for

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# from dotenv import load_dotenv
# import os

# load_dotenv()

# sender_email = os.getenv("sender_email")
# password = os.getenv("password")

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    phonenumber = db.Column(db.String(80))
    email = db.Column(db.String(200))
    password = db.Column(db.String(80))
    active = db.Column(db.Boolean())
    status  = db.Column(db.Integer ) #not verified is 1 and 2 is verified and 3 is admin
    subscription_id = db.Column(db.String())
    expiry_date =  db.Column(db.String())
    created_date = db.Column(db.String())
    dateTime = db.Column(db.DateTime, default=datetime.datetime.now())
    
    photoURL = db.Column(db.String(100))
    profession = db.Column(db.String())
    location = db.Column(db.String())
    links = db.Column(db.String())
    jobsApplied = db.Column(db.String(), default="{'ids': [] }" ) # an array of job ids
    skills = db.Column(db.String()) # an array of skills
    about = db.Column(db.String())
    

    def __init__(self, email, phonenumber, name, location, active, profession, links,phototURL):
        
        self.email = email
        # self.password = password
        self.phonenumber = phonenumber
        self.name = name
        self.location = location
        self.active = active
        self.profession = profession
        self.links = links
        self.photoURL = phototURL


    def json(self):
        return {
            'id': self.id,
            'email': self.email,
            'phonenumber': self.phonenumber,
            'name': self.name,
            'photoURL': self.photoURL,
            'location': self.location,
            'profession': self.profession,
            'links': self.links,
            'jobsApplied': self.jobsApplied,
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

    def send_verification_email(self, receiver_email, token):

        print("mail")

        sender_email = "t8910ech@gmail.com"
        password = "8910@tech"
        # receiver_email = receiver_email

        # msg = Message('Confirm Email', sender=sender_email, recipients=receiver_email)

        link = url_for('emailverification', token=token, _external=True)

        # msg.body = 'Your link is {}'.format(link)

        # mail.send(msg)

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
            <a href="{}" text-decoration="none"> here</a> 
             to verify.
            </p>
        </body>
        </html>
        """.format(link)

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
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_phonenumber(cls, phonenumber):
        return cls.query.filter_by(phonenumber=phonenumber).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

