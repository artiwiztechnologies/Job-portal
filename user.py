from db import db
import datetime
import requests


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200))
    password = db.Column(db.String(80))
    status  = db.Column(db.Integer ) #not verified is 1 and 2 is verified and 3 is admin
    phonenumber = db.Column(db.String(80))
    dateTime = db.Column(db.DateTime, default=datetime.datetime.now())
    tempotp  = db.Column(db.Integer ) #not verified is 1 and 2 is verified and 3 is admin


    def __init__(self, email,password,status,phonenumber,tempotp):
        self.email = email
        self.password = password
        self.status = status
        self.phonenumber = phonenumber
        self.tempotp = tempotp


    def json(self):
        return {
            'id': self.id,
            'email': self.email
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def send_otp(self):
        requests.get("http://trans.smsfresh.co/api/sendmsg.php?user=hkartthik97&pass=123456&sender=ARTOTP&phone={}&text=Your verfication code is:{} Dont share this code with anyone.&priority=ndnd&stype=normal".format(self.phonenumber,self.tempotp))


    @classmethod
    def find_by_username(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_phonenumber(cls, phonenumber):
        return cls.query.filter_by(phonenumber=phonenumber).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

