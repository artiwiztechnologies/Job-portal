from db import db
import datetime
import requests

from models.orders import OrdersModel
from models.user import UserModel


class PaymentsModel(db.Model):

    __tablename__ = "payments"

    pid = db.Column(db.Integer(), primary_key=True)
    oid = db.Column(db.Integer())
    user_id = db.Column(db.Integer())
    email = db.Column(db.String())
    phonenumber = db.Column(db.String())
    plan_id = db.Column(db.Integer())
    user_type = db.Column(db.String())
    razorpay_payment_id = db.Column(db.String())
    razorpay_order_id = db.Column(db.String())
    razorpay_signature = db.Column(db.String())

    def __init__(self, pid, oid, user_id, email, plan_id, phonenumber, user_type, razorpay_payment_id, razorpay_order_id, razorpay_signature):

        self.pid = pid
        self.oid = oid
        self.user_id = user_id
        self.email = email
        self.plan_id = plan_id
        self.phonenumber = phonenumber
        self.user_type = user_type
        self.razorpay_payment_id = razorpay_payment_id
        self.razorpay_order_id = razorpay_order_id

    def json(self):

        order = OrdersModel.find_by_id(self.oid)

        if not order:
            return {'message': 'order not found'}

        return {
            'payment_id': self.pid,
            'order_id': self.oid,
            'user_id': self.user_id,
            'user_type': self.user_type,
            'email': self.email,
            'phonenumber': self.phonenumber,
            'amount': order.amount/100,
            'status': order.status,
            'razorpay_payment_id': self.razorpay_payment_id,
            'razorpay_order_id': self.razorpay_order_id
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_pid(cls, pid):
        return cls.query.filter_by(pid=pid).first()

    @classmethod
    def find_by_oid(cls, oid):
        return cls.query.filter_by(oid=oid).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()
