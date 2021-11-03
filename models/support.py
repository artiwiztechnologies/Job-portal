from db import db
import datetime
import requests

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# SENDER_EMAIL = "noreply@artiwiztech.com"
# PASSWORD = "Polgara!@12"

from dotenv import load_dotenv
import os

load_dotenv()

sender_email = os.getenv("SENDER_EMAIL")
password = os.getenv("PASSWORD")


class SupportModel(db.Model):

    __tableaname__ = "support"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    name = db.Column(db.String())
    email = db.Column(db.String())
    phonenumber = db.Column(db.String())
    user_type = db.Column(db.String())
    title = db.Column(db.String())
    description = db.Column(db.String())

    def __init__(self, user_id, name, email, phonenumber, user_type, title, description):

        self.user_id = user_id
        self.name = name
        self.email = email
        self.phonenumber = phonenumber
        self.user_type = user_type
        self.title = title
        self.description = description

    def json(self):

        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'email': self.email,
            'phonenumber': self.phonenumber,
            'user_type': self.user_type,
            'description': self.description,
            'title': self.title,
            'message': self.message
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def send_support_email(self, data):

        receiver_email1 = "felixjordan312@gmail.com"
        receiver_email1 = "support@artiwiztechnologies.zohodesk.in"

        message = MIMEMultipart("alternative")
        message["Subject"] = "Issue"
        message["From"] = sender_email
        message["To"] = receiver_email

        html = """\
            <h3>Issues raised by: {} ({})</h3>
            <h4>Phonenumber: {}</h4>
            <h4>Email: {}</h4>
            <h4>Title: {}</h4>
            <p>Description: {}</p>
            """.format(data['name'], data['user_type'], data['phonenumber'], data['email'], data['title'], data['description'])

        part = MIMEText(html, "html")

        message.attach(part)

        # message = render_template("verification_email.html")

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.hostinger.in", 465, context=context) as server:
            # server.starttls(context=context)
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )
