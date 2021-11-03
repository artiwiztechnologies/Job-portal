from db import db
import datetime
import requests


class AdminModel(db.Model):

    __tablename__ = "admin"

    id = db.Column(db.Integer(), primary_key=True)
    phonenumber = db.Column(db.String())
    name = db.Column(db.String())
    email = db.Column(db.String())
    password = db.Column(db.String())
    active = db.Column(db.Boolean(), default=False)
    status = db.Column(db.Integer())

    def __init__(self, name, email, phonenumber):
        self.name = name
        self.email = email
        self.phonenumber = phonenumber

    def json(self):

        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phonenumber': self.phonenumber,
            'active': self.active,
            'status': self.status
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_phonenumber(cls, phonenumber):
        return cls.query.filter_by(phonenumber=phonenumber).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
