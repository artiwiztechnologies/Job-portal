from db import db
import datetime
import requests

class payOrdersModel(db.Model):

    __tablename__ = "payment_orders"

    id = db.Column(db.Integer(), primary_key=True)
    oid = db.Column(db.String(15))
    user_id = db.Column(db.Integer())
    email = db.Column(db.String())
    user_type = db.Column(db.String())
    plan_id = db.Column(db.Integer())

    amount = db.Column(db.Integer())
    currency = db.Column(db.String())
    status = db.Column(db.String())
    dateTime = db.Column(db.String, default=datetime.datetime.now())
    checksumhash = db.Column(db.String())
    db.UniqueConstraint(oid)


    # offer_id, notes, plan_id not stored in db.

    def __init__(self, oid, user_id, email, user_type, amount, currency, status, plan_id, root):

        self.oid = oid
        self.user_id = user_id
        self.email = email
        self.user_type = user_type
        self.plan_id = plan_id

        self.amount = amount
        self.currency = currency
        self.status = status

    def json(self):

        return {
            "id":self.id,
            "order_id": self.oid,
            "user_id": self.user_id,
            "email": self.email,
            "user_type": self.user_type,
            'plan_id': self.plan_id,

            "amount": self.amount,
            "currency": self.currency,
            "status": self.status,
            "dateTime": self.dateTime
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, oid):
        return cls.query.filter_by(oid=oid).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()
