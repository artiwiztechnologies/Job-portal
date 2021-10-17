from db import db
import datetime
import requests


class OrdersModel(db.Model):

    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    email = db.Column(db.String())
    user_type = db.Column(db.String())

    _id = db.Column(db.String())
    entity = db.Column(db.String())
    amount = db.Column(db.Integer)
    amount_paid = db.Column(db.Integer)
    amount_due = db.Column(db.Integer)
    currency = db.Column(db.String())
    receipt = db.Column(db.String())
    # offer_id = db.Column(db.Integer)
    status = db.Column(db.String())
    attempts = db.Column(db.Integer)
    created_at = db.Column(db.Integer)

    def __init__(self, user_id, email, user_type, id, entity, amount, amount_paid, amount_due, currency, receipt, status, attempts, created_at, offer_id, notes, plan_id):

        self.user_id = user_id
        self.email = email
        self.user_type = user_type

        self._id = id
        self.entity = entity
        self.amount = amount
        self.amount_paid = amount_paid
        self.amount_due = amount_due
        self.currency = currency
        self.receipt = receipt
        # self.offer_id = offer_id
        self.status = status
        self.attempts = attempts
        self.created_at = created_at

    def json(self):

        return {
            "id": self.id,
            "user_id": self.user_id,
            "email": self.email,
            "user_type": self.user_type,

            "order_id": self._id,
            "entity": self.entity,
            "amount": self.amount,
            "amount_paid": self.amount_paid,
            "amount_due": self.amount_due,
            "currency": self.currency,
            "receipt": self.receipt,
            "status": self.status,
            "attempts": self.attempts,
            "created_at": self.attempts
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
