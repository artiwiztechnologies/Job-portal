from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
import random
import requests
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_refresh_token_required, get_jwt_identity, jwt_required, get_raw_jwt
from random import randrange
import datetime

from models.company import CompanyModel
from models.helper import Helper
from models.jobs import JobsModel
from models.plans import PlansModel
from models.applications import ApplicationsModel
from models.user import UserModel
from blacklist import BLACKLIST

from flask import request, jsonify, send_file, send_from_directory, url_for, redirect
from werkzeug.utils import secure_filename
import os
import re
import json

from itsdangerous import URLSafeTimedSerializer, SignatureExpired
s = URLSafeTimedSerializer('Thisisasecret!')

UPLOAD_FOLDER = 'companyphoto'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


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
        _company_parser.add_argument('password',
                                     type=str,
                                     required=True,
                                     help="This field cannot be blank."
                                     )
        _company_parser.add_argument('active',
                                     type=bool,
                                     required=True,
                                     help="This field cannot be blank."
                                     )
        _company_parser.add_argument('location',
                                     type=str,
                                     required=False,
                                     default="",
                                     help="This field cannot be blank."
                                     )
        _company_parser.add_argument('about',
                                     type=str,
                                     required=False,
                                     default="",
                                     help="This field cannot be blank."
                                     )
        _company_parser.add_argument('links',
                                     type=str,
                                     required=False,
                                     default="",
                                     help="This field cannot be blank."
                                     )
        _company_parser.add_argument('about',
                                     type=str,
                                     required=False,
                                     default="",
                                     help="This field cannot be blank."
                                     )
        _company_parser.add_argument('established',
                                     type=str,
                                     required=False,
                                     default="",
                                     help="This field cannot be blank."
                                     )
        _company_parser.add_argument('companyType',
                                     type=str,
                                     required=False,
                                     default="",
                                     help="This field cannot be blank."
                                     )
        _company_parser.add_argument('companySize',
                                     type=int,
                                     required=False,
                                     default=0,
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

            token = s.dumps(data['email'], salt='email-confirm')

            company = CompanyModel(data['email'], data['phonenumber'], data['name'], data['location'],
                                   data['status'], data['companySize'], data['about'], data['links'], data['established'], data['companyType'])
            company.status = 1
            company.password = data['password']
            company.save_to_db()
            company.send_verification_email(company, token)

            return {"message": "Company created successfully."}, 201


class companyemailVerification(Resource):
    def get(self, token):
        try:
            email = s.loads(token, salt='email-confirm', max_age=300)
            company = CompanyModel.find_by_companyemail(email)
            company.status = 8
            company.save_to_db()
        except SignatureExpired:
            return '<h1>The token is expired!</h1>'
        return redirect("https://jobportalfrontend.vercel.app/", code=302)


class resendCompanyEmail(Resource):
    def get(self, id):
        company = CompanyModel.find_by_id(id)
        if not company:
            return {'message': 'Company not found!!'}, 400
        token = s.dumps(company.email, salt='email-confirm')
        company.send_verification_email(company, token)

        return {'message': 'Verification mail sent!'}, 200


class CompanyPhoto(Resource):

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
                company_id = get_jwt_identity()
                company = CompanyModel.find_by_id(company_id)

                if company.photoURL != "":
                    print(UPLOAD_FOLDER + "/" +
                          company.photoURL.split('/')[-1])
                    try:
                        os.remove(UPLOAD_FOLDER + "/" +
                                  company.photoURL.split('/')[-1])
                    except:
                        pass
                    company.photoURL = ""
                    company.save_to_db()
                filename = secure_filename(file.filename)

                URL = request.url_root[:-1]
                print(True)
                print(URL)
                photoURL = "company" + str(company_id) + "-" + filename

                file.save(os.path.join(UPLOAD_FOLDER, photoURL))

                company.photoURL = URL + "/company/" + photoURL
                company.save_to_db()
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
            return {'message': "Success", "photoURL": company.photoURL}
        else:
            resp = jsonify(errors)
            resp.status_code = 500
            return resp

    @jwt_required
    def delete(self):
        company_id = get_jwt_identity()
        # print(user_id)
        company = CompanyModel.find_by_id(company_id)
        try:
            photo = company.photoURL.split('/')[-1]
            print(photo)
            os.remove(UPLOAD_FOLDER+"/"+photo)
            company.photoURL = ""
            company.save_to_db()
            return {'message': 'Photo deleted.'}, 200
        except:
            pass
        return {'message': 'Photo not uploaded.'}, 404


class getCompanyPhoto(Resource):
    def get(self, path):
        print(path)
        try:
            return send_from_directory(UPLOAD_FOLDER, path=path, as_attachment=True)
        except FileNotFoundError:
            return {'message': 'File not Found'}, 404


class Company(Resource):
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
    _company_parser.add_argument('location',
                                 type=str,
                                 required=True,
                                 help="This field cannot be blank."
                                 )
    _company_parser.add_argument('about',
                                 type=str,
                                 required=True,
                                 help="This field cannot be blank."
                                 )
    _company_parser.add_argument('links',
                                 type=str,
                                 required=True,
                                 help="This field cannot be blank."
                                 )
    _company_parser.add_argument('about',
                                 type=str,
                                 required=True,
                                 help="This field cannot be blank."
                                 )
    _company_parser.add_argument('established',
                                 type=str,
                                 required=True,
                                 help="This field cannot be blank."
                                 )
    _company_parser.add_argument('companyType',
                                 type=str,
                                 required=True,
                                 help="This field cannot be blank."
                                 )
    _company_parser.add_argument('companySize',
                                 type=int,
                                 required=True,
                                 help="This field cannot be blank."
                                 )

    """
    This resource can be useful when testing our Flask app. We may not want to expose it to public users, but for the
    sake of demonstration in this course, it can be useful when we are manipulating data regarding the users.
    """

    @jwt_required
    def get(self, id):
        company = CompanyModel.find_by_id(id)
        if not company:
            return {'message': 'Company Not Found'}, 404
        return company.json(), 200

    @jwt_required
    def delete(self, id):
        company = CompanyModel.find_by_id(id)
        if not company:
            return {'message': 'Company Not Found'}, 404

        Helper.del_applications_by_company(id)
        Helper.del_jobs_by_company(id)
        Helper.del_products_by_company(id)
        company.delete_from_db()
        return {'message': 'Company deleted.'}, 200

    @jwt_required
    def put(self, id):
        data = Company._company_parser.parse_args()
        if not CompanyModel.find_by_id(id):
            return {'message': 'Company not found.'}, 404
        company = CompanyModel.find_by_id(id)

        # print(company.com)

        company.name = data['name']
        company.phonenumber = data['phonenumber']
        company.email = data['email']
        company.location = data['location']
        company.companySize = data['companySize']
        company.about = data['about']
        company.companyType = data['companyType']
        company.links = data['links']

        company.save_to_db()

        return {'message': 'Update successful!'}, 200


class EditCompany(Resource):

    @jwt_required
    def put(self):

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
        _company_parser.add_argument('location',
                                     type=str,
                                     required=True,
                                     help="This field cannot be blank."
                                     )
        _company_parser.add_argument('about',
                                     type=str,
                                     required=True,
                                     help="This field cannot be blank."
                                     )
        _company_parser.add_argument('links',
                                     type=str,
                                     required=True,
                                     help="This field cannot be blank."
                                     )
        _company_parser.add_argument('about',
                                     type=str,
                                     required=True,
                                     help="This field cannot be blank."
                                     )
        _company_parser.add_argument('established',
                                     type=str,
                                     required=True,
                                     help="This field cannot be blank."
                                     )
        _company_parser.add_argument('companyType',
                                     type=str,
                                     required=True,
                                     help="This field cannot be blank."
                                     )
        _company_parser.add_argument('companySize',
                                     type=int,
                                     required=True,
                                     help="This field cannot be blank."
                                     )

        data = _company_parser.parse_args()

        id = get_jwt_identity()

        if not CompanyModel.find_by_id(id):
            return {'message': 'User not found.'}, 404
        company = CompanyModel.find_by_id(id)

        company.name = data['name']
        company.phonenumber = data['phonenumber']
        company.email = data['email']
        company.location = data['location']
        company.comapanySize = data['companySize']
        company.about = data['about']
        company.companyType = data['companyType']
        company.links = data['links']

        company.save_to_db()

        return {'message': 'Update successful!'}, 200

    @jwt_required
    def delete(self):

        id = get_jwt_identity()

        company = CompanyModel.find_by_id(id)
        if not company:
            return {'message': 'User Not Found'}, 404

        Helper.del_applications_by_company(id)
        Helper.del_jobs_by_company(id)
        Helper.del_favorites_by_company(id)
        company.delete_from_db()
        return {'message': 'User deleted.'}, 200


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
        if company:
            if safe_str_cmp(company.password, data['password']):
                if(company.status == 2):
                    access_token = create_access_token(
                        identity=company.id, fresh=True)
                    refresh_token = create_refresh_token(company.id)
                    return {
                        'access_token': access_token,
                        'refresh_token': refresh_token,
                        'company_id': company.id,
                        "email": company.email,
                        'status': company.status,
                        'type': company.__tablename__,
                        'active': company.active,
                        'expiry_date': company.expiry_date
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
                    token = s.dumps(company.email, salt='email-confirm')

                    company.save_to_db()
                    company.send_verification_email(company, token)

                    return{"message": "Account not verified", "status": company.status, "id": company.id}, 401
                elif(company.status == 8):

                    return{"message": "Waiting for admin approval.", "status": company.status, "id": company.id}, 401

            
            return {"message": "Invalid Credentials!"}, 401
        return {"message": "Company not found!", "status": 0}, 404


class CompanyLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        BLACKLIST.add(jti)
        return {"message": "Successfully logged out"}, 200


class CompanyTokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        """
        Get a new access token without requiring username and password???only the 'refresh token'
        provided in the /login endpoint.

        Note that refreshed access tokens have a `fresh=False`, which means that the user may have not
        given us their username and password for potentially a long time (if the token has been
        refreshed many times over).
        """
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200


class ForgotCompanyPassword(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('phonenumber',
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                            )
        data = parser.parse_args()

        company = CompanyModel.find_by_phonenumber(data['phonenumber'])

        if not company:
            return {'message': 'Company not found'}, 404

        otp = randrange(100000, 1000000)

        company.otp = str(otp)
        company.save_to_db()
        receiver_email = company.email

        # print(otp)
        company.send_otp_email(str(otp), receiver_email, company.phonenumber)
        return {'message': 'OTP sent'}, 200


class ResetCompanyPassword(Resource):

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

        company = CompanyModel.find_by_phonenumber(data['phonenumber'])

        if not company:
            return {'message': 'Company not found'}, 404

        if data['otp'] != company.otp:
            return {'message': 'Wrong OTP!'}, 400

        if data['oldpassword'] != company.password:
            return {'message': 'Wrong password!'}, 400

        if data['password'] == company.password:
            return {'message': 'New password cannot be the same as the old password'}, 400

        company.password = data['password']
        company.save_to_db()

        return {'message': 'Password successfuly reset.'}, 200


class getCompanyCount(Resource):

    def get(self):
        try:
            total = CompanyModel.find_count()
            return {"total": total}, 200
        except:
            return {'message': 'Error'}, 500


class getJobsNames(Resource):

    @jwt_required
    def get(self):

        company_id = get_jwt_identity()
        jobs = JobsModel.find_by_company_id(company_id)

        if not jobs:
            return {'message': 'No jobs posted.'}, 404

        titles = []

        for job in jobs:
            titles.append(job.title)

        return {'titles': titles}, 200


class CheckCompany(Resource):

    @jwt_required
    def get(self):

        company_id = get_jwt_identity()

        company = CompanyModel.find_by_id(company_id)

        if not company:
            return {'message': 'No such company.'}, 404

        # if company.active:

        #     today1 = str(datetime.datetime.now()).split(' ')[0][2:]
        #     # today1 = "31-10-19"
        #     today = str(datetime.datetime.strptime(today1, "%y-%m-%d"))

        #     d = company.expiry_date
        #     d1 = datetime.date(int(d[:4]), int(d[5:7]), int(d[8:10]))
        #     d2 = datetime.date(int(today[:4]), int(
        #         today[5:7]), int(today[8:10]))

        #     delta = d1-d2

        #     if(today > company.expiry_date):
        #         company.active = False
        #         company.save_to_db()

        # if company.active:
        #     plan = PlansModel.find_by_id(company.plan_id)
        #     return {'status': company.status, 'active': company.active, 'days': delta.days, "plan_name": plan.plan_name}, 200
        return {'status': company.status, 'active': company.active}, 200


class Applicants(Resource):

    @jwt_required
    def get(self):
        try:
            company_id = get_jwt_identity()
            if not CompanyModel.find_by_id(company_id):
                return {'message': 'Company not founs'}, 404
            applications_main = [application.json(
            ) for application in ApplicationsModel.find_by_company_id(company_id)]

            applications = ApplicationsModel.find_by_company_id(company_id)

            if not applications:
                return {'message': 'No users have applied to this company'}, 401

            applicants = []
            for application in applications:
                user = UserModel.find_by_id(application.user_id)
                applicants.append(user.json1(application.json()))
            return {'Applicants': applicants}
        except:
            return {'message': 'Error'}, 500
