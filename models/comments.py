from db import db
import datetime
import requests
from models.user import UserModel
from models.company import CompanyModel


class CommentsModel(db.Model):

    __tablename__ = "comments"

    id = db.Column(db.Integer(), primary_key=True)
    question_id = db.Column(db.Integer())
    user_id = db.Column(db.Integer())
    user_type = db.Column(db.String(6))
    user_name = db.Column(db.String())  # remove
    user_photo = db.Column(db.String())  # remove
    comment = db.Column(db.String())
    date = db.Column(db.String(), default=str(
        datetime.datetime.now()).split(' ')[0])

    def __init__(self, user_id, user_type, question_id, comment):
        if user_type == 'users':
            user = UserModel.find_by_id(user_id)
        else:
            user = CompanyModel.find_by_id(user_id)

        self.user_id = user_id
        self.user_type = user_type
        self.user_name = user.name
        self.user_photo = user.photoURL
        self.question_id = question_id
        self.comment = comment

    def json(self):

        if self.user_type == 'users':
            user = UserModel.find_by_id(self.user_id)
        else:
            user = CompanyModel.find_by_id(self.user_id)

        return {
            'id': self.id,
            'user_id': self.user_id,
            'user_type': self.user_type,
            'user_name': user.name,
            'user_photo': user.photoURL,
            'question_id': self.question_id,
            'comment': self.comment,
            'date': self.date
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
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_question_id(cls, question_id):
        return cls.query.filter_by(question_id=question_id)
