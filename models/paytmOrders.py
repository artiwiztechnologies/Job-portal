from db import db
import datetime
import requests


class OrdersModel(db.Model):

    __tablename__ = "paytmOrders"

    oid = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer())
    email = db.Column(db.String())
    user_type = db.Column(db.String())
    plan_id = db.Column(db.Integer())

    order_id = db.Column(db.String(15))
    amount = db.Column(db.Integer())
    currency = db.Column(db.String())
    status = db.Column(db.String())
    created_at = db.Column(db.Integer())



    def __init__(self, oid, user_id, email, user_type, amount, currency, status, plan_id):

        self.user_id = user_id
        self.email = email
        self.user_type = user_type
        self.plan_id = plan_id

        self.order_id = oid
        self.amount = amount
        self.currency = currency
        self.status = status

    def json(self):

        return {
            "id": self.oid,
            "user_id": self.user_id,
            "email": self.email,
            "user_type": self.user_type,
            'plan_id': self.plan_id,

            "order_id": self.order_id,
            "amount": self.amount,
            "currency": self.currency,
            "status": self.status,
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

    @classmethod
    def find_by_orderid(cls, orderid):
        return cls.query.filter_by(order_id=orderid).first()