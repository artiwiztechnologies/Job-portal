from db import db
import datetime
import requests
from flask import Flask, request, url_for

from templates.email import Email
from templates.otp import OTP_email

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from dotenv import load_dotenv
import os

load_dotenv()

sender_email = os.getenv("SENDER_EMAIL")
password = os.getenv("PASSWORD")


class CompanyModel(db.Model):

    __tablename__ = 'company'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    phonenumber = db.Column(db.String())
    email = db.Column(db.String())
    password = db.Column(db.String())
    active = db.Column(db.Boolean(), default=True)
    subscription_id = db.Column(db.String())
    expiry_date = db.Column(db.String())
    created_date = db.Column(db.String())
    status = db.Column(db.Integer)
    dateTime = db.Column(db.DateTime, default=datetime.datetime.now())
    otp = db.Column(db.String(6))
    plan_id = db.Column(db.Integer())
    trial_availed = db.Column(db.Boolean(), default=False)

    photoURL = db.Column(db.String(), default="abcd")
    location = db.Column(db.String())
    companySize = db.Column(db.Integer(), default=0)
    about = db.Column(db.String())
    links = db.Column(db.String())
    established = db.Column(db.String())
    # an array of job ids
    jobsPosted = db.Column(db.String(), default="{'ids': [] }")
    companyType = db.Column(db.String())

    def __init__(self, email, phonenumber, name, location, status, companySize, about, links, established, companyType):
        self.email = email
        self.phonenumber = phonenumber
        self.name = name
        self.status = status
        # self.active = active

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
            'companySize': self.companySize,
            'about': self.about,
            'established': self.established,
            'jobsPosted': self.jobsPosted,
            'companyType': self.companyType,
            'links': self.links,
            'status': self.status,
            'active': self.active,
            'type': self.__tablename__,
            'expiry_date': self.expiry_date
        }

    def json_for_admin(self):

        if self.status == 2:
            STATUS = 'Active'
        elif self.status == 1:
            STATUS = 'Inactive'

        return {
            'id': self.id,
            'name': self.name,
            'phonenumber': self.phonenumber,
            'email': self.email,
            'expiry_date': self.expiry_date[:10] if self.expiry_date else "-",
            'plan_id': self.plan_id if self.plan_id else "-",
            'status': STATUS,
            'subs': "Subscribed" if self.plan_id else "Not subscribed"
        }

    def send_verification_email(self, receiver_email, token):

        link = url_for('companyemailverification', token=token, _external=True)

        message = MIMEMultipart("alternative")
        message["Subject"] = "Jobs Textile - Verfication email."
        message["From"] = sender_email
        message["To"] = receiver_email

        html = Email._email(link)

        part2 = MIMEText(html, "html")

        message.attach(part2)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.hostinger.in", 465, context=context) as server:
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

    @classmethod
    def find_count(cls):
        return cls.query.count()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def send_otp_email(self, otp, receiver_email, phonenumber):

        message = MIMEMultipart("alternative")
        message["Subject"] = "Jobs Textile - OTP for Two Factor Authentication (2FA)."
        message["From"] = sender_email
        message["To"] = receiver_email

        # html = Email._email(link)

        # html = """\
        #     <p>Your OTP is {}.</p>
        #     """.format(otp)

        try:
            num = phonenumber[:2]+"******"+phonenumber[-2:]
        except:
            num = phonenumber
        html = OTP_email.OTP(num, otp)

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
