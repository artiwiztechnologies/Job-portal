from db import db
import datetime
import requests
from flask import Flask, request, url_for

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class CompanyModel(db.Model):

    __tablename__ = 'company'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    phonenumber = db.Column(db.String())
    email = db.Column(db.String())
    password = db.Column(db.String())
    active = db.Column(db.String())
    subscription_id = db.Column(db.String())
    expiry_date = db.Column(db.String())
    created_date = db.Column(db.String())
    status = db.Column(db.Integer)
    dateTime = db.Column(db.DateTime, default=datetime.datetime.now())

    photoURL = db.Column(db.String(), default="abcd")
    location = db.Column(db.String())
    comapanySize = db.Column(db.Integer)
    about = db.Column(db.String())
    links = db.Column(db.String())
    established = db.Column(db.String())
    jobsPosted = db.Column(db.String(), default="{'ids': [] }") # an array of job ids
    companyType = db.Column(db.String())


    def __init__(self, email, phonenumber, name, location, active, status, companySize, about, links, established, companyType):
        self.email = email
        self.phonenumber = phonenumber
        self.name = name
        self.status = status
        self.active = active

        self.location = location
        self.companySize = companySize
        self.about = about
        self.links = links
        self.established = established
        self.companyType = companyType


    def json(self):
        return {
            'id': self.id,
            'email': self.email,
            'phonenumber': self.phonenumber,
            'name': self.name,
            'photoURL': self.photoURL,
            'location': self.location,
            'companySize': self.comapanySize,
            'about': self.about,
            'established': self.established,
            'jobsPosted': self.jobsPosted,
            'companyType': self.companyType,
            'links': self.links,
            'status': self.status,
            'type': self.__tablename__
        }

    def send_verification_email(self, receiver_email, token):

        print("mail")

        sender_email = "t8910ech@gmail.com"
        password = "8910@tech"
        # receiver_email = receiver_email

        link = url_for('companyemailverification', token=token, _external=True)

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

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_companyemail(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_phonenumber(cls, phonenumber):
        return cls.query.filter_by(phonenumber=phonenumber).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()