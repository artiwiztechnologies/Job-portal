from db import db
import datetime
import requests


class PlansModel(db.Model):
    __tablename__ = "plans"

    id = db.Column(db.Integer(), primary_key=True)
    plan_name = db.Column(db.String())
    plan_rate = db.Column(db.Float())
    duration = db.Column(db.Integer())  # in days
    trial = db.Column(db.Boolean())
    tax = db.Column(db.Integer())
    description = db.Column(db.String())

    def __init__(self, plan_name, plan_rate, duration, trial, tax, description):
        self.plan_name = plan_name
        self.plan_rate = plan_rate
        self.duration = duration
        self.trial = trial
        self.tax = tax
        self.description = description

    def json(self):


        return {
            "id": self.id,
            "plan_name": self.plan_name,
            "plan_rate": self.plan_rate,
            "duration": self.duration,
            "trial": self.trial,
            "tax": self.tax,
            "description": self.description.split(',')
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
    def find_by_plan_name(cls, plan_name):
        return cls.query.filter_by(plan_name=plan_name).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()
