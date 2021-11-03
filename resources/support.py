from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
import requests
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_refresh_token_required, get_jwt_identity, jwt_required, get_raw_jwt

from models.support import SupportModel
from models.user import UserModel
from models.company import CompanyModel


class newSupport(Resource):

    @jwt_required
    def post(self):

        parser = reqparse.RequestParser()

        parser.add_argument('title',
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                            )
        parser.add_argument('description',
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                            )
        parser.add_argument('user_type',
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                            )

        data = parser.parse_args()

        jwt_id = get_jwt_identity()
        data['user_id'] = jwt_id

        if data['description'] == "" or data['title'] == "":
            return {'message': 'Enter valid title and description.'}, 401

        if data['user_type'] == "users":

            user = UserModel.find_by_id(jwt_id)
            data['name'] = user.name
            data['email'] = user.email
            data['phonenumber'] = user.phonenumber

        else:

            company = CompanyModel.find_by_id(jwt_id)
            data['name'] = company.name
            data['email'] = company.email
            data['phonenumber'] = company.phonenumber

        try:
            support = SupportModel(**data)
            support.send_support_email(data)
            support.save_to_db()
        except:
            return {'message': 'Issue could not be raised.'}, 500

        return {'message': 'Issue raised successfuly.'}, 200
