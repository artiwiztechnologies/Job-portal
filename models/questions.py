from db import db
import datetime
import requests
from models.user import UserModel
from models.company import CompanyModel
from models.comments import CommentsModel


class QuestionsModel(db.Model):

    __tablename__ = "questions"

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer())
    user_type = db.Column(db.String(6))
    user_name = db.Column(db.String())
    user_photo = db.Column(db.String())
    question = db.Column(db.String())
    date = db.Column(db.String(), default=str(
        datetime.datetime.now()).split(' ')[0])

    def __init__(self, user_id, user_type, question):
        if user_type == 'users':
            user = UserModel.find_by_id(user_id)
        else:
            user = CompanyModel.find_by_id(user_id)

        self.user_id = user_id
        self.user_type = user_type
        self.user_name = user.name
        self.user_photo = user.photoURL
        self.question = question

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
            'question': self.question,
            'date': self.date
        }

    def question_json(self, id):

        comments = [comment.json()
                    for comment in CommentsModel.find_by_question_id(id)]

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
            'question': self.question,
            'date': self.date,
            'comments': comments
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
    def find_by_question(cls, question):
        return cls.query.filter_by(question=question).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_user_type(cls, user_id, user_type):
        return cls.query.filter_by(user_id=user_id, user_type=user_type)
