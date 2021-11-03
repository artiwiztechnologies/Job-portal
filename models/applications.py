from db import db
import datetime
import requests

from models.user import UserModel
from models.jobs import JobsModel
from models.company import CompanyModel


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


class ApplicationsModel(db.Model):
    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user_name = db.Column(db.String)
    user_email = db.Column(db.String(), db.ForeignKey('users.email'))
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'))
    company_name = db.Column(db.String())
    company_id = db.Column(db.Integer(), db.ForeignKey('company.id'))
    status = db.Column(db.String(), default="applied")
    date = db.Column(db.String, default=str(
        datetime.datetime.now()).split(' ')[0])

    def __init__(self, user_name, user_id, user_email, job_id, company_id, company_name):
        self.user_id = user_id
        self.user_email = user_email
        self.job_id = job_id
        self.company_id = company_id
        self.user_name = user_name
        self.company_name = company_name

    def json(self):
        if JobsModel.find_by_id(self.job_id):
            title = JobsModel.find_by_id(self.job_id).title
        else:
            title = "Job has been deleted."

        return {
            "id": self.id,
            "user_id": self.user_id,
            "user_name": self.user_name,
            "user_email": self.user_email,
            "job_id": self.job_id,
            "company_id": self.company_id,
            "job_title": title,
            'status': self.status,
            "date": self.date
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
    def find_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id)

    @classmethod
    def find_by_company_id(cls, company_id):
        return cls.query.filter_by(company_id=company_id)

    @classmethod
    def find_by_user_email(cls, user_email):
        return cls.query.filter_by(user_email=user_email)

    @classmethod
    def find_by_job_id(cls, job_id):
        return cls.query.filter_by(job_id=job_id)

    @classmethod
    def find_by_job_user(cls, job_id, user_id):
        return cls.query.filter_by(job_id=job_id, user_id=user_id).first()

    @classmethod
    def find_applicants_count(cls, job_id):
        return cls.query.filter_by(job_id=job_id).count()

    @classmethod
    def find_count(cls):
        return cls.query.count()

    def send_rejection_email(self, user, job, company):

        receiver_email = user.email

        message = MIMEMultipart("alternative")
        message["Subject"] = "Regarding job application."
        message["From"] = sender_email
        message["To"] = receiver_email

        html = """\
            <p>Dear {},</p>
            <p>Thank you for taking the time to apply for the {} role.</p>
            <p>It was a pleasure to learn more about your skills and accomplishments. </p>
            <p>Unfortunately, our team did not select you for further consideration.</p>
            <p>{}</p>
            """.format(user.name, job, company)

        part = MIMEText(html, "html")

        message.attach(part)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.hostinger.in", 465, context=context) as server:
            # server.starttls(context=context)
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )
