from db import db
import datetime
import requests

from models.company import CompanyModel


class JobsModel(db.Model):
    __tablename__ = "jobs"

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    title = db.Column(db.String(80))
    description = db.Column(db.String(500))
    applicants = db.Column(db.String()) # to be deleted
    available = db.Column(db.Boolean())
    date = db.Column(db.String, default=str(
        datetime.datetime.now()).split(' ')[0])
    job_type = db.Column(db.String())
    salary = db.Column(db.String())
    career_level = db.Column(db.String())
    role = db.Column(db.String())
    skills = db.Column(db.String())

    def __init__(self, company_id, title, description, applicants, available, job_type, salary, career_level, role, skills):
        self.company_id = company_id
        self.title = title
        self.description = description
        self.applicants = applicants
        self.available = available
        self.job_type = job_type
        self.salary = salary
        self.career_level = career_level
        self.role = role
        self.skills = skills

    def json(self):
        return {
            "id": self.id,
            "title": self.title,
            "company_id": self.company_id,
            "description": self.description,
            # "applicants": self.applicants,
            "available": self.available,
            "job_type": self.job_type,
            "salary": self.salary,
            "career_level": self.career_level,
            "role": self.role,
            "skills": self.skills,
            "date": self.date,
            "photoURL": CompanyModel.find_by_id(self.company_id).photoURL,
            "location": CompanyModel.find_by_id(self.company_id).location,
            "company_name": CompanyModel.find_by_id(self.company_id).name,
            "company_size": CompanyModel.find_by_id(self.company_id).companySize,
            "company_type": CompanyModel.find_by_id(self.company_id).companyType

        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_title(cls, title):
        return cls.query.filter_by(title=title).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_count(cls):
        return cls.query.count()

    @classmethod
    def find_jobs(cls, id):
        return cls.query.filter_by(company_id=id)

    @classmethod
    def find_by_company_id(cls, company_id):
        return cls.query.filter_by(company_id=company_id)

    @classmethod
    def find_job_user(cls, job_id, user_id):
        return cls.query.filter_by(user_id=user_id, job_id=job_id).first()