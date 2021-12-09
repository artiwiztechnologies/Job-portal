from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from random import randrange
import requests
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_refresh_token_required, get_jwt_identity, jwt_required, get_raw_jwt
import datetime

from models.comments import CommentsModel
from models.questions import QuestionsModel
from models.user import UserModel
from models.company import CompanyModel


class newComment(Resource):

    @jwt_required
    def post(self):

        parser = reqparse.RequestParser()

        parser.add_argument('user_type',
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                            )
        parser.add_argument('comment',
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                            )
        parser.add_argument('question_id',
                            type=int,
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

        if not QuestionsModel.find_by_id(data['question_id']):
            return {'message': 'Question not found.'}, 404

        try:
            comment = CommentsModel(**data)
            comment.save_to_db()
            return {'message': 'Answer posted!'}, 200

        except:
            return {'message': 'error'}, 201
