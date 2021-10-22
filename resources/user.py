from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
import random
import requests
import datetime
from random import randrange

from flask import request, jsonify, send_file, send_from_directory, url_for, redirect, render_template
from werkzeug.utils import secure_filename
import os
import re
import json

from flask_jwt_extended import create_access_token, create_refresh_token, jwt_refresh_token_required, get_jwt_identity, jwt_required, get_raw_jwt

from models.user import UserModel
from blacklist import BLACKLIST

from itsdangerous import URLSafeTimedSerializer, SignatureExpired

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from dotenv import load_dotenv
import os

load_dotenv()

sender_email = os.getenv("SENDER_EMAIL")
password = os.getenv("PASSWORD")

UPLOAD_FOLDER = 'candidatephoto'
RESUME_FOLDER = 'resume'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
ALLOWED_EXTENSIONS2 = set(['docx', 'doc', 'pdf'])


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
        _user_parser.add_argument('about',
                                  type=str,
                                  required=False,
                                  default="",
                                  help="This field cannot be blank."
                                  )

        data = _user_parser.parse_args()
        # print(data['phonenumber'])
        if UserModel.find_by_phonenumber(data['phonenumber']):
            return {"message": "A user with that phone already exists"}, 400
        elif UserModel.find_by_email(data['email']):
            return {"message": "A user with that email already exists"}, 400
        else:
            token = s.dumps(data['email'], salt='email-confirm')

            user = UserModel(data['email'], data['phonenumber'], data['name'], data['location'],
                             data['active'], data['profession'], data['links'], data['about'])
            user.status = data['status']
            user.password = data['password']
            user.save_to_db()
            user.send_verification_email(data['email'], token)

            return {"message": "User created successfully."}, 201


class emailVerification(Resource):
    def get(self, token):
        try:
            email = s.loads(token, salt='email-confirm', max_age=300)
            user = UserModel.find_by_email(email)

            user.status = 2
            user.save_to_db()

        except SignatureExpired:

            # h = """\
            #     <h1>hello</h1>
            #     """
            # return h

            return "Invalid token"

        return redirect("https://jobportalfrontend.vercel.app/", code=302)


class resendEmail(Resource):
    def get(self, id):
        user = UserModel.find_by_id(id)
        if not user:
            return {'message': "User not found!"}, 400
        token = s.dumps(user.email, salt='email-confirm')
        user.send_verification_email(user.email, token)

        return {'message': 'Verification mail sent!'}, 200


class UserPhoto(Resource):
    @jwt_required
    def post(self):

        # print(request.files)
        if 'file' not in request.files:
            return {'message': 'No file uploaded!'}, 400

        files = request.files.getlist('file')
        errors = {}
        success = False
        for file in files:
            if file and '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
                user_id = get_jwt_identity()
                user = UserModel.find_by_id(user_id)

                if user.photoURL != "":
                    print(UPLOAD_FOLDER + "/" + user.photoURL.split('/')[-1])
                    try:
                        os.remove(UPLOAD_FOLDER + "/" + user.photoURL.split('/')[-1])
                    except:
                        pass
                    user.photoURL = ""
                    user.save_to_db()
                ext = secure_filename(file.filename).rsplit('.', 1)[1].lower()
                filename = secure_filename(file.filename)

                URL = request.url_root[:-1]
                print(True)
                print(URL)
                photoURL = "user"+ str(user_id) + "-" + filename

                file.save(os.path.join(UPLOAD_FOLDER, photoURL))

                user.photoURL = URL + "/user/" + photoURL
                user.save_to_db()
                success = True

            else:
                errors[file.filename] = 'File type is not allowed'

        if success and errors:
            errors['message'] = 'File(s) successfully uploaded'
            resp = jsonify(errors)
            resp.status_code = 500
            return resp
        if success:
            resp = jsonify({'message': 'Files successfully uploaded'})
            resp.status_code = 201
            return {'message': "Success", "photoURL": user.photoURL}
        else:
            resp = jsonify(errors)
            resp.status_code = 500
            return resp

    @jwt_required
    def delete(self):
        user_id = get_jwt_identity()
        print(user_id)
        user = UserModel.find_by_id(user_id)
        try:
            photo = user.photoURL.split('/')[-1]
            print(photo)
            os.remove(UPLOAD_FOLDER+"/"+photo)
            user.photoURL = ""
            user.save_to_db()
            return {'message': 'Photo deleted.'}, 200
        except:
            pass
        return {'message': 'Photo not uploaded.'}, 404


class getUserPhoto(Resource):
    def get(self, path):
        print(path)
        try:
            return send_from_directory(UPLOAD_FOLDER, path=path, as_attachment=True)
        except FileNotFoundError:
            return {'message': 'File not Found'}, 404


class Resume(Resource):
    @jwt_required
    def post(self):

        if 'file' not in request.files:
            return {'message': 'No file uploaded!'}, 404

        files = request.files.getlist('file')
        errors = {}
        for file in files:
            if file and '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS2:
                user_id = get_jwt_identity()
                user = UserModel.find_by_id(user_id)

                if user.resume != "":
                    try:
                        os.remove(RESUME_FOLDER + "/" + user.resume.split('/')[-1])
                    except:
                        pass
                    user.resume = ""
                    user.save_to_db()
                filename = secure_filename(file.filename)

                URL = request.url_root[:-1]
                resume = "resume"+ str(user_id) + "-" + filename

                file.save(os.path.join(RESUME_FOLDER, resume))

                user.resume = URL + "/user-resume/" + resume
                user.save_to_db()
                success = True

                return {'message': 'success', "resume": user.resume}

            else:
                return {'message': 'error'}

    @jwt_required
    def delete(self):
        user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)
        for EXT in ALLOWED_EXTENSIONS2:
            try:
                filename = user.resume.split('/')[-1]
                print(filename)
                os.remove(RESUME_FOLDER+"/"+filename)
                user.resume = ""
                user.save_to_db()
                return {'message': "Resume deleted."}, 200
            except:
                return {'message': 'Resume not uploaded.'}, 404


class getResume(Resource):
    def get(self, path):
        print(path)
        try:
            return send_from_directory(RESUME_FOLDER, path=path)
        except FileNotFoundError:
            return {'message': 'File not Found'}, 404


class User(Resource):
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
    _user_parser.add_argument('about',
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
        user.about = data['about']

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
        if user:
            if safe_str_cmp(user.password, data['password']):
                if(user.status == 2):
                    access_token = create_access_token(
                        identity=user.id, fresh=True)
                    refresh_token = create_refresh_token(user.id)
                    return {
                        'access_token': access_token,
                        'refresh_token': refresh_token,
                        'user_id': user.id,
                        "email": user.email,
                        "status": user.status,
                        'type': user.__tablename__,
                        'active': user.active,
                        'expiry_date': user.expiry_date
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
                    token = s.dumps(user.email, salt='email-confirm')

                    user.save_to_db()
                    print(user.id)
                    user.send_verification_email(user.email, token)

                    return{"message": "Account not verified", "status": user.status, "id": user.id}, 401
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


class ExpireUser(Resource):
    @jwt_required
    def post(self):
        user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)
        if user.active:

            today1 = str(datetime.datetime.now()).split(' ')[0][2:]
            # today1 = "31-10-19"
            today = str(datetime.datetime.strptime(today1, "%y-%m-%d"))

            # expiry_date = datetime.datetime.strptime(
            #     user.expiry_date[2:10], "%y-%m-%d")

            if(today > user.expiry_date):
                user.active = False
                user.save_to_db()
                return {'active': False, 'message': 'Subscription expired!'}

            return {'active': True, 'message': 'Subscription not expired!'}
        return {'active': False, 'message': 'No active subscription'}


class ForgotUserPassword(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('phonenumber',
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                            )
        data = parser.parse_args()

        user = UserModel.find_by_phonenumber(data['phonenumber'])

        if not user:
            return {'message': 'User not found'}, 404

        otp = randrange(100000, 1000000)

        user.otp = str(otp)
        user.save_to_db()
        receiver_email = user.email

        # print(otp)
        user.send_otp_email(str(otp), receiver_email)
        return {'message': 'OTP sent'}, 200


class ResetUserPassword(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('phonenumber',
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                            )
        parser.add_argument('password',
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                            )
        parser.add_argument('oldpassword',
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                            )
        parser.add_argument('otp',
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                            )
        data = parser.parse_args()

        user = UserModel.find_by_phonenumber(data['phonenumber'])

        if not user:
            return {'message': 'User not found'}, 404

        if data['otp'] != user.otp:
            return {'message': 'Wrong OTP!'}, 400

        if data['oldpassword'] != user.password:
            return {'message': 'Wrong password!'}, 400

        if data['password'] == user.password:
            return {'message': 'New password cannot be the same as the old password'}, 400

        user.password = data['password']
        user.save_to_db()

        return {'message': 'Password successfuly reset.'}, 200



# class Resume(Resource):
#     @jwt_required
#     def post(self):

#         def delete_file(EXT):
#             user_id = get_jwt_identity()
#             filename = str(user_id)+"."+EXT
#             os.remove(RESUME_FOLDER+"/"+filename)

#         if 'file' not in request.files:
#             return {'message': 'No file uploaded!'}, 404

#         files = request.files.getlist('file')
#         errors = {}
#         for file in files:
#             if file and '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS2:
#                 user_id = get_jwt_identity()

#                 ext = secure_filename(file.filename).rsplit('.', 1)[1].lower()
#                 print(ext)

#                 filename = str(user_id)+"."+ext
#                 for EXT in ALLOWED_EXTENSIONS2:
#                     path = str(user_id)+"."+EXT
#                     try:
#                         send_from_directory(RESUME_FOLDER, path=path)
#                         delete_file(EXT)
#                         print(True)
#                     except:
#                         print(False)

#                 file.save(os.path.join(RESUME_FOLDER, filename))

#                 URL = request.url_root[:-1]
#                 # print(URL, 146)
#                 resume = URL+"/user/resume/"+filename

#                 user = UserModel.find_by_id(user_id)
#                 user.resume = resume
#                 user.save_to_db()

#                 return {'message': 'success', "resume": resume}

#             else:
#                 return {'message': 'error'}

#     @jwt_required
#     def delete(self):
#         user_id = get_jwt_identity()
#         user = UserModel.find_by_id(user_id)
#         for EXT in ALLOWED_EXTENSIONS2:
#             try:
#                 filename = str(user_id)+"."+EXT
#                 print(filename)
#                 os.remove(RESUME_FOLDER+"/"+filename)
#                 user.resume = ""
#                 user.save_to_db()
#                 return {'message': "Resume deleted."}, 200
#             except:
#                 return {'message': 'Resume not uploaded.'}, 404