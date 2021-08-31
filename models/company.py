from db import db
import datetime
import requests

class CompanyModel(db.Model):

    __tablename__ = 'company'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    phonenumber = db.Column(db.String())
    photoURL = db.Column(db.String())
    email = db.Column(db.String())
    password = db.Column(db.String())
    active = db.Column(db.String())
    address = db.Column(db.String())
    subscription_id = db.Column(db.String())
    expiry_date = db.Column(db.String())
    created_date = db.Column(db.String())
    status = db.Column(db.Integer)
    dateTime = db.Column(db.DateTime, default=datetime.datetime.now())

    def __init__(self, email, password, phonenumber, name, photoURL, address, active, status):
        self.email = email
        self.password = password
        self.status = status
        self.phonenumber = phonenumber
        self.name = name
        self.photoURL = photoURL
        self.address = address
        self.active = active

    def json(self):
        return {
            'id': self.id,
            'email': self.email,
            'phonenumber': self.phonenumber,
            'name': self.name,
            'photoURL': self.photoURL,
            'address': self.address
        }

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