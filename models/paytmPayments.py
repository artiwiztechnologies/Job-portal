from db import db
import datetime
import requests

from models.orders import OrdersModel
from models.user import UserModel


class PaymentsModel(db.Model):

    __tablename__ = "paytmPayments"

    pid = db.Column(db.Integer(), primary_key=True)
    order_id = db.Column(db.Integer())
    user_id = db.Column(db.Integer())
    email = db.Column(db.String())
    phonenumber = db.Column(db.String())
    plan_id = db.Column(db.Integer())
    user_type = db.Column(db.String())
    payment_id = db.Column(db.String())

    def __init__(self, pid, oid, user_id, email, plan_id, phonenumber, user_type):

        self.order_id = oid
        self.user_id = user_id
        self.email = email
        self.plan_id = plan_id
        self.phonenumber = phonenumber
        self.user_type = user_type
        self.payment_id = pid
        # self.razorpay_order_id = razorpay_order_id

    def json(self):

        order = OrdersModel.find_by_id(self.order_id)

        if not order:
            return {'message': 'Order not found'}

        return {
            'payment_id': self.pid,
            'order_id': self.order_id,
            'user_id': self.user_id,
            'user_type': self.user_type,
            'email': self.email,
            'phonenumber': self.phonenumber,
            'amount': order.amount,
            'status': order.status
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
    def find_by_oid(cls, order_id):
        return cls.query.filter_by(order_id=order_id).first()

    @classmethod
    def find_by_orderid(cls, orderid):
        return cls.query.filter_by(order_id=orderid).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()
