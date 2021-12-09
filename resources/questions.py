from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from random import randrange
import requests
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_refresh_token_required, get_jwt_identity, jwt_required, get_raw_jwt
import datetime

from models.questions import QuestionsModel
from models.user import UserModel
from models.company import CompanyModel
from models.helper import Helper


class newQuestion(Resource):

    @jwt_required
    def post(self):

        parser = reqparse.RequestParser()

        parser.add_argument('user_type',
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                            )
        parser.add_argument('question',
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                            )

        data = parser.parse_args()

        data['user_id'] = get_jwt_identity()

        if not (CompanyModel.find_by_id(data["user_id"]) or UserModel.find_by_id(data["user_id"])):
            return {'message': 'User not found'}, 404

        if data["user_type"] == 'users':
            user = UserModel.find_by_id(data["user_id"])
        else:
            user = CompanyModel.find_by_id(data["user_id"])

        if not user.active:
            return {'message': 'User does not have an active plan.'}

        try:
            question = QuestionsModel(**data)
            question.save_to_db()
            return {'message': 'Question posted!'}, 200

        except:
            return {'message': 'error'}, 201


class Question(Resource):

    @jwt_required
    def get(self, id):

        try:
            question = QuestionsModel.find_by_id(id)
            return {'question': question.question_json(id)}
        except:
            return {'message': 'Error'}, 500

    @jwt_required
    def put(self, id):

        parser = reqparse.RequestParser()

        parser.add_argument('question',
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                            )

        data = parser.parse_args()

        if not QuestionsModel.find_by_id(id):
            return {'message': 'No such question found.'}, 404

        try:
            question = QuestionsModel.find_by_id(id)
            question.question = data['question']
            question.save_to_db()
            return {'message': 'Question updated successefuly.'}, 200
        except:
            return{'message': 'error'}, 201

    @jwt_required
    def delete(self, id):

        if not QuestionsModel.find_by_id(id):
            return {'message': 'No such question found.'}, 404

        try:
            question = QuestionsModel.find_by_id(id)
            question.delete_from_db()

            Helper.del_comments_by_question(id)

            return {'message': 'Question deleted successfuly.'}, 200

        except:
            return {'message': 'error'}, 201


class QuestionsList(Resource):

    @jwt_required
    def get(self):

        try:
            questions = [question.json()
                         for question in QuestionsModel.find_all()]
            return {'Questions': questions}, 200

        except:

            return {'message': 'Error'}, 500


class PostedQuestions(Resource):

    @jwt_required
    def get(self, user_type):

        try:
            user_id = get_jwt_identity()
            questions = [question.json()
                         for question in QuestionsModel.find_by_user_type(user_id, user_type)]
            return {'Questions': questions}, 200

        except:

            return {'message': 'Error'}, 500
