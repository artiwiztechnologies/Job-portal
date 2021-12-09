from db import db
import datetime
import requests


class SubscriptionsModel(db.Model):

    __tablename__ = "subscriptions"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    plan = db.Column(db.String())
    start_date = db.Column(db.String())
    end_date = db.Column(db.String())
    amount = db.Column(db.Float())
    transaction_date = db.Column(db.String(), default=str(
        datetime.datetime.now()).split(' ')[0])
    subscriber_type = db.Column(db.String())
    active = db.Column(db.Boolean(), default=True)

    def __init__(self, user_id, plan, start_date, end_date, amount, subscriber_type):
        self.user_id = user_id
        self.plan = plan
        self.start_date = start_date
        self.end_date = end_date
        self.amount = amount
        self.subscriber_type = subscriber_type

    def json(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "plan": self.plan,
            "amount": self.amount,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "transaction_date": self.transaction_date,
            "subscriber_type": self.subscriber_type,
            "active": self.active
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
    def find_by_user_id_type(cls, user_id, _type):
        return cls.query.filter_by(user_id=user_id)

    @classmethod
    def find_one(cls, user_id, _type):
        return cls.query.filter_by(user_id=user_id, subscriber_type=_type).first()
