from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
import random
import requests
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_refresh_token_required, get_jwt_identity, jwt_required, get_raw_jwt

from models.company import CompanyModel
from blacklist import BLACKLIST

class CompanyRegister(Resource):
    def post(self):
        _company_parser = reqparse.RequestParser()

        _company_parser.add_argument('name',
                                  type=str,
                                  required=True,
                                  help="This field cannot be blank."
                                  )
        _company_parser.add_argument('phonenumber',
                                  type=str,
                                  required=True,
                                  help="This field cannot be blank."
                                  )
        _company_parser.add_argument('email',
                                  type=str,
                                  required=True,
                                  help="This field cannot be blank."
                                  )
        _company_parser.add_argument('address',
                                  type=str,
                                  required=True,
                                  help="This field cannot be blank."
                                  )
        _company_parser.add_argument('password',
                                  type=str,
                                  required=True,
                                  help="This field cannot be blank."
                                  )
        _company_parser.add_argument('photoURL',
                                  type=str,
                                  required=False,
                                  help="This field cannot be blank."
                                  )
        _company_parser.add_argument('active',
                                  type=bool,
                                  required=True,
                                  help="This field cannot be blank."
                                  )
        _company_parser.add_argument('status',
                                  type=int,
                                  required=True,
                                  help="This field cannot be blank."
                                  )

        data = _company_parser.parse_args()

        if CompanyModel.find_by_phonenumber(data['phonenumber']):
            return {'message': 'A user with that phone already exists.'}, 400
        elif CompanyModel.find_by_companyemail(data['email']):
            return {'message': 'A user with that email already exists.'}, 400
        else:

            user_phonenumber = data['phonenumber']
            rand_number = random.randint(1111, 9999)
            # data['tempotp'] = rand_number
            user = CompanyModel(**data)
            # user.send_otp()
            user.save_to_db()

            return {"message": "Company created successfully."}, 201

# class UserResendOTP(Resource):
#     def post(self):
#         _user_parser = reqparse.RequestParser()
#         _user_parser.add_argument('phonenumber',
#                                   type=str,
#                                   required=True,
#                                   help="This field cannot be blank."
#                                   )
#         data = _user_parser.parse_args()
#         user = UserModel.find_by_phonenumber(data['phonenumber'])

#         if user:
#             user_phonenumber = data['phonenumber']
#             rand_number = random.randint(1111, 9999)
#             user.tempotp = rand_number
#             user.save_to_db()
#             user.send_otp()
#             return {"message": "OTP resent successfully."}, 200
#         else:
#             return {"message": "User not found."}, 400

class Company(Resource):
    _user_parser = reqparse.RequestParser()
    """
    This resource can be useful when testing our Flask app. We may not want to expose it to public users, but for the
    sake of demonstration in this course, it can be useful when we are manipulating data regarding the users.
    """

    @jwt_required
    def get(self, id):
        company = CompanyModel.find_by_id(id)
        if not company:
            return {'message': 'User Not Found'}, 404
        return company.json(), 200

    @jwt_required
    def delete(self, id):
        company = CompanyModel.find_by_id(id)
        if not company:
            return {'message': 'User Not Found'}, 404
        company.delete_from_db()
        return {'message': 'User deleted.'}, 200

class CompanyConfirmation(Resource):
    def post(self):
        _company_parser = reqparse.RequestParser()

        _company_parser.add_argument('phonenumber',
                                  type=str,
                                  required=True,
                                  help="This field cannot be blank."
                                  )

        _company_parser.add_argument('tempotp',
                                  type=int,
                                  required=True,
                                  help="This field cannot be blank."
                                  )
        data = _company_parser.parse_args()
        company = CompanyModel.find_by_phonenumber(data['phonenumber'])
        companytempotpdb = str(user.tempotp)
        companytempotpuser = str(data['tempotp'])
        if company and safe_str_cmp(companytempotpdb, companytempotpuser):
            company.status = 2

            company.save_to_db()

            return {"message": "Account verified", "status": company.status}, 200

        return {"message": "Invalid OTP"}, 401

class CompanyLogin(Resource):
    def post(self):
        _company_parser = reqparse.RequestParser()
        _company_parser.add_argument('phonenumber',
                                  type=str,
                                  required=True,
                                  help="This field cannot be blank."
                                  )
        _company_parser.add_argument('password',
                                  type=str,
                                  required=True,
                                  help="This field cannot be blank."
                                  )
        data = _company_parser.parse_args()

        company = CompanyModel.find_by_phonenumber(data['phonenumber'])
        # print(company.password, data['password'])
        # print(safe_str_cmp(company.password, data['password']))
        # this is what the `authenticate()` function did in security.py
        if company:
            if safe_str_cmp(company.password, data['password']):
                # identity= is what the identity() function did in security.py—now stored in the JWT
                if(company.status == 2):
                    access_token = create_access_token(
                        identity=company.id, fresh=True)
                    refresh_token = create_refresh_token(company.id)
                    return {
                        'access_token': access_token,
                        'refresh_token': refresh_token,
                        'company_id': company.id,
                        "email": company.email
                    }, 200
                elif(company.status == 3):
                    access_token = create_access_token(
                        identity=company.id, fresh=True)
                    refresh_token = create_refresh_token(company.id)
                    return {
                        'access_token': access_token,
                        'refresh_token': refresh_token,
                        'company_id': company.id,
                        "email": company.email,
                        "status": 3
                    }, 200
                elif(company.status == 1):
                    rand_number = random.randint(1111, 9999)
                    company.tempotp = rand_number
                    company.save_to_db()
                    company.send_otp()

                    return{"message": "Account not verified", "status": company.status}, 401
            return {"message": "Invalid Credentials!"}, 401
        return {"message": "Company not found!", "status": 0}, 404

class CompanyLogout(Resource):
    @jwt_required
    def post(self):
        # jti is "JWT ID", a unique identifier for a JWT.
        jti = get_raw_jwt()['jti']
        BLACKLIST.add(jti)
        return {"message": "Successfully logged out"}, 200

class CompanyTokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        """
        Get a new access token without requiring username and password—only the 'refresh token'
        provided in the /login endpoint.

        Note that refreshed access tokens have a `fresh=False`, which means that the user may have not
        given us their username and password for potentially a long time (if the token has been
        refreshed many times over).
        """
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200
