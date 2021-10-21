from db import db
import datetime
import requests
from flask import Flask, request, url_for, render_template

from templates.email import Email
from templates.otp import OTP_email

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from random import randrange

from dotenv import load_dotenv
import os

load_dotenv()

sender_email = os.getenv("SENDER_EMAIL")
password = os.getenv("PASSWORD")

# sender_email = "t8910ech@gmail.com"
# password = "8910@tech"


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    phonenumber = db.Column(db.String(80))
    email = db.Column(db.String(200))
    password = db.Column(db.String(80))
    active = db.Column(db.Boolean(), default=False)
    # not verified is 1 and 2 is verified and 3 is admin
    status = db.Column(db.Integer)
    subscription_id = db.Column(db.String())
    expiry_date = db.Column(db.String())
    created_date = db.Column(db.String())  # have to remove
    dateTime = db.Column(db.DateTime, default=datetime.datetime.now())
    otp = db.Column(db.String(6))

    photoURL = db.Column(db.String(100), default="abcd")
    profession = db.Column(db.String())
    location = db.Column(db.String())
    links = db.Column(db.String())
    jobsApplied = db.Column(
        db.String(), default="{'ids': [] }")  # have to remove
    skills = db.Column(db.String())  # an array of skills
    about = db.Column(db.String())
    resume = db.Column(db.String(100), default="abcd")

    def __init__(self, email, phonenumber, name, location, active, profession, links, about):

        self.email = email
        # self.password = password
        self.phonenumber = phonenumber
        self.name = name
        self.location = location
        # self.active = active
        self.profession = profession
        self.links = links
        self.about = about

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
            'status': self.status,
            'resume': self.resume,
            'type': self.__tablename__,
            'about': self.about,
            'active': self.active,
            'expiry_date': self.expiry_date
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_phonenumber(cls, phonenumber):
        return cls.query.filter_by(phonenumber=phonenumber).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def send_verification_email(self, receiver_email, token):

        link = url_for('emailverification', token=token, _external=True)

        message = MIMEMultipart("alternative")
        message["Subject"] = "Verfication email."
        message["From"] = sender_email
        message["To"] = receiver_email

        html = Email._email(link)

        part2 = MIMEText(html, "html")

        message.attach(part2)

        # message = render_template("verification_email.html")

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.hostinger.in", 465, context=context) as server:
            # server.starttls(context=context)
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )

    def send_otp_email(self, otp, receiver_email):

        # sender_email = "t8910ech@gmail.com"
        # password = "8910@tech"

        message = MIMEMultipart("alternative")
        message["Subject"] = "Reset password."
        message["From"] = sender_email
        message["To"] = receiver_email

        # html = Email._email(link)

        html = """\
            <p>Your OTP is {}.</p>
            """.format(otp)

        # html = OTP_email.OTP(otp)

        # print(receiver_email)
        part2 = MIMEText(html, "html")

        message.attach(part2)

        # message = render_template("verification_email.html")

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.hostinger.in", 465, context=context) as server:
            # server.starttls(context=context)
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )
