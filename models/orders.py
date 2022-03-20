from db import db
import datetime
import requests


class OrdersModel(db.Model):

    __tablename__ = "orders"

    oid = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer())
    email = db.Column(db.String())
    user_type = db.Column(db.String())
    plan_id = db.Column(db.Integer())
    # _type = db.Column(db.String())

    order_id = db.Column(db.String(15))
    entity = db.Column(db.String())
    amount = db.Column(db.Integer())
    amount_paid = db.Column(db.Integer())
    amount_due = db.Column(db.Integer())
    currency = db.Column(db.String())
    receipt = db.Column(db.String())
    # offer_id = db.Column(db.Integer)
    status = db.Column(db.String())
    attempts = db.Column(db.Integer())
    created_at = db.Column(db.Integer())
    checksumhash = db.Column(db.String())

    # db.UniqueConstraint(order_id)

    # offer_id, notes, plan_id not stored in db.

    def __init__(self, oid, user_id, email, user_type, amount, currency, status, plan_id, root, checksumhash):

        self.user_id = user_id
        self.email = email
        self.user_type = user_type
        self.plan_id = plan_id

        self.order_id = oid
        # self.entity = entity
        self.amount = amount
        self.checksumhash = checksumhash
        # self.amount_paid = amount_paid
        # self.amount_due = amount_due
        self.currency = currency
        # self.receipt = receipt
        # self.offer_id = offer_id
        self.status = status
        # self.attempts = attempts
        # self.created_at = created_at

    def json(self):

        return {
            "id": self.oid,
            "user_id": self.user_id,
            "email": self.email,
            "user_type": self.user_type,
            'plan_id': self.plan_id,

            "order_id": self.order_id,
            # "entity": self.entity,
            "amount": self.amount,
            # "amount_paid": self.amount_paid/100,
            # "amount_due": self.amount_due/100,
            "currency": self.currency,
            # "receipt": self.receipt,
            "status": self.status,
            # "attempts": self.attempts,
            # "created_at": self.created_at
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


{
    "id": "order_IA5Dr8YNgIdMul",
    "entity": "order",
    "amount": 500,
    "amount_paid": 0,
    "amount_due": 500,
    "currency": "INR",
    "receipt": "order_rcptid_11",
    "offer_id": None,
    "status": "created",
    "attempts": 0,
    "notes": [],
    "created_at": 1634403754
}
