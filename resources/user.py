from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
import random
import requests
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_refresh_token_required, get_jwt_identity, jwt_required, get_raw_jwt

from models.user import UserModel
from blacklist import BLACKLIST

from itsdangerous import URLSafeTimedSerializer, SignatureExpired

# import smtplib, ssl
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# app = Flask(__name__)
# user.config.from_pyfile('../config.cfg')
# app.config.from_pyfile('config.cfg')
# _user_parser = reqparse.RequestParser()

s = URLSafeTimedSerializer('Thisisasecret!')
class UserRegister(Resource):


    def post(self):
        _user_parser = reqparse.RequestParser()

        _user_parser.add_argument('name',
                                  type=str,
                                  required=True,
                                  help="This field cannot be blank."
                                  )
        _user_parser.add_argument('phonenumber',
                                  type=str,
                                  required=True,
                                  help="This field cannot be blank."
                                  )
        _user_parser.add_argument('email',
                                  type=str,
                                  required=True,
                                  help="This field cannot be blank."
                                  )
        _user_parser.add_argument('password',
                                  type=str,
                                  required=True,
                                  help="This field cannot be blank."
                                  )
        _user_parser.add_argument('active',
                                  type=bool,
                                  required=True,
                                  help="This field cannot be blank."
                                  )
        _user_parser.add_argument('location',
                                  type=str,
                                  required=False,
                                  default="",
                                  help="This field cannot be blank."
                                  )
        _user_parser.add_argument('profession',
                                    type=str,
                                    required=False,
                                    default="",
                                    help="This field cannot be blank."
                                    )
        _user_parser.add_argument('links',
                                    type=str,
                                    required=False,
                                    default="",
                                    help="This field cannot be blank."
                                    )
        _user_parser.add_argument('status',
                                  type=int,
                                  required=True,
                                  help="This field cannot be blank."
                                  )

        data = _user_parser.parse_args()
        print(data['phonenumber'])
        if UserModel.find_by_phonenumber(data['phonenumber']):
            return {"message": "A user with that phone already exists"}, 400
        elif UserModel.find_by_phonenumber(data['email']):
            return {"message": "A user with that phonenumber already exists"}, 400
        else:
            
            
            token = s.dumps(data['email'], salt='email-confirm')

            user = UserModel(data['email'], data['phonenumber'], data['name'], data['location'], data['active'], data['profession'], data['links'])
            user.status = data['status']
            user.password = data['password']
            user.save_to_db()
            print(user.id)
            user.send_verification_email(data['email'], token)

            # print(token)

            return {"message": "User created successfully."}, 201

    
class emailVerfication(Resource):
    def get(self, token):
        try:
            email = s.loads(token, salt='email-confirm', max_age=300)
            user = UserModel.find_by_email(email)
            user.status = 2
            user.save_to_db()
        except SignatureExpired:
            return '<h1>The token is expired!</h1>'
        return '<h1>Verified<h1>'
        # return '<h1>The token works!</h1>'
        
        
    

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


class User(Resource):
    # _user_parser = reqparse.RequestParser()
    """
    This resource can be useful when testing our Flask app. We may not want to expose it to public users, but for the
    sake of demonstration in this course, it can be useful when we are manipulating data regarding the users.
    """
    _user_parser = reqparse.RequestParser()

    _user_parser.add_argument('name',
                                type=str,
                                required=True,
                                help="This field cannot be blank."
                                )
    _user_parser.add_argument('phonenumber',
                                type=str,
                                required=True,
                                help="This field cannot be blank."
                                )
    _user_parser.add_argument('email',
                                type=str,
                                required=True,
                                help="This field cannot be blank."
                                )
    _user_parser.add_argument('location',
                                type=str,
                                required=True,
                                help="This field cannot be blank."
                                )
    _user_parser.add_argument('profession',
                                type=str,
                                required=True,
                                help="This field cannot be blank."
                                )
    _user_parser.add_argument('links',
                                type=str,
                                required=True,
                                help="This field cannot be blank."
                                )
    _user_parser.add_argument('jobsApplied',
                                type=str,
                                required=True,
                                help="This field cannot be blank."
                                )
    


    @jwt_required
    def get(self, id):
        print('yes')
        user = UserModel.find_by_id(id)
        if not user:
            return {'message': 'User Not Found'}, 404
        return user.json(), 200

    @jwt_required
    def delete(self, id):
        user = UserModel.find_by_id(id)
        if not user:
            return {'message': 'User Not Found'}, 404
        user.delete_from_db()
        return {'message': 'User deleted.'}, 200

    @jwt_required
    def put(self, id):
        data = User._user_parser.parse_args()
        if not UserModel.find_by_id(id):
            return {'message': 'User not found.'}, 404
        user = UserModel.find_by_id(id)

        user.name = data['name']
        user.phonenumber = data['phonenumber']
        user.email = data['email']
        user.location = data['location']
        user.profession = data['profession']
        user.jobsApplied = data['jobsApplied']
        user.links = data['links']

        user.save_to_db()

        return {'message': 'Update successful!'}, 200
        



class UserLogin(Resource):
    def post(self):
        _user_parser = reqparse.RequestParser()
        _user_parser.add_argument('phonenumber',
                                  type=str,
                                  required=True,
                                  help="This field cannot be blank."
                                  )
        _user_parser.add_argument('password',
                                  type=str,
                                  required=True,
                                  help="This field cannot be blank."
                                  )
        data = _user_parser.parse_args()

        user = UserModel.find_by_phonenumber(data['phonenumber'])
        # print(user.password, data['password'])
        # print(safe_str_cmp(user.password, data['password']))
        # this is what the `authenticate()` function did in security.py
        if user:
            if safe_str_cmp(user.password, data['password']):
                # identity= is what the identity() function did in security.py—now stored in the JWT
                if(user.status == 2):
                    access_token = create_access_token(
                        identity=user.id, fresh=True)
                    refresh_token = create_refresh_token(user.id)
                    return {
                        'access_token': access_token,
                        'refresh_token': refresh_token,
                        'user_id': user.id,
                        "email": user.email
                    }, 200
                elif(user.status == 3):
                    access_token = create_access_token(
                        identity=user.id, fresh=True)
                    refresh_token = create_refresh_token(user.id)
                    return {
                        'access_token': access_token,
                        'refresh_token': refresh_token,
                        'user_id': user.id,
                        "email": user.email,
                        "status": 3
                    }, 200
                elif(user.status == 1):
                    token = s.dumps(user['email'], salt='email-confirm')

                    # user = UserModel(**data)
                    # user.token = token
                    user.save_to_db()
                    print(user.id)
                    user.send_verification_email(user['email'], token)


                    return{"message": "Account not verified", "status": user.status}, 401
            return {"message": "Invalid Credentials!"}, 401
        return {"message": "User not found!", "status": 0}, 404


class UserLogout(Resource):
    @jwt_required
    def post(self):
        # jti is "JWT ID", a unique identifier for a JWT.
        jti = get_raw_jwt()['jti']
        BLACKLIST.add(jti)
        return {"message": "Successfully logged out"}, 200


class TokenRefresh(Resource):
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
