from db import db
import datetime
import requests

from models.user import UserModel
from models.jobs import JobsModel
from models.company import CompanyModel


class FavoritesModel(db.Model):
    __tablename__ = "favorites"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer())
    user_email = db.Column(db.String())
    job_id = db.Column(db.Integer())
    company_id = db.Column(db.Integer())
    date = db.Column(db.String, default=str(
        datetime.datetime.now()).split(' ')[0])

    def __init__(self, user_id, user_email, job_id, company_id):

        job = JobsModel.find_by_id(job_id)
        self.user_id = user_id
        self.user_email = user_email
        self.job_id = job_id
        self.company_id = job.company_id

    def json(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "user_email": self.user_email,
            "job_id": self.job_id,
            "company_id": self.company_id,
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
    def find_by_user_email(cls, user_email):
        return cls.query.filter_by(user_email=user_email)

    @classmethod
    def find_by_job_id(cls, job_id):
        return cls.query.filter_by(job_id=job_id)

    @classmethod
    def find_by_job_user(cls, job_id, user_id):
        return cls.query.filter_by(job_id=job_id, user_id=user_id).first()

    @classmethod
    def find_by_company_id(cls, company_id):
        return cls.query.filter_by(company_id=company_id)
