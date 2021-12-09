from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
import requests
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_refresh_token_required, get_jwt_identity, jwt_required, get_raw_jwt

from models.admin import AdminModel
from models.user import UserModel
from models.favorites import FavoritesModel
from models.jobs import JobsModel
from models.company import CompanyModel
from models.applications import ApplicationsModel


class newAdmin(Resource):

    def post(self):

        admin_parser = reqparse.RequestParser()

        admin_parser.add_argument('name',
                                  type=str,
                                  required=True,
                                  help="This field cannot be blank."
                                  )
        admin_parser.add_argument('phonenumber',
                                  type=str,
                                  required=True,
                                  help="This field cannot be blank."
                                  )
        admin_parser.add_argument('email',
                                  type=str,
                                  required=True,
                                  help="This field cannot be blank."
                                  )
        admin_parser.add_argument('password',
                                  type=str,
                                  required=True,
                                  help="This field cannot be blank."
                                  )

        data = admin_parser.parse_args()

        if AdminModel.find_by_phonenumber(data['phonenumber']):
            return {'message': "Phonenumber already exits."}, 401

        if AdminModel.find_by_email(data['email']):
            return {'message': "Email already exits."}, 401

        admin = AdminModel(data['name'], data['email'], data['phonenumber'])
        admin.status = 3
        admin.password = data['password']

        admin.save_to_db()

        return {'message': 'Admin created successfuly.'}, 200


class AdminLogin(Resource):

    def post(self):
        admin_parser = reqparse.RequestParser()

        admin_parser.add_argument('phonenumber',
                                  type=str,
                                  required=True,
                                  help="This field cannot be blank."
                                  )
        admin_parser.add_argument('password',
                                  type=str,
                                  required=True,
                                  help="This field cannot be blank."
                                  )

        data = admin_parser.parse_args()

        admin = AdminModel.find_by_phonenumber(data['phonenumber'])

        if not admin:
            return {'message': 'Admin not found.'}, 404

        if not safe_str_cmp(admin.password, data['password']):
            return {'message': 'Invalid credentials'}, 401

        if admin.status != 3:
            return {'message': 'Not an admin.'}, 401

        else:
            access_token = create_access_token(
                identity=admin.id, fresh=True)
            refresh_token = create_refresh_token(admin.id)

            return {
                'access_token': access_token,
                'refresh_token': refresh_token,
                'admin_id': admin.id,
                "email": admin.email,
                "status": admin.status,
                'type': admin.__tablename__,
                'active': admin.active
            }, 200


class SendMetrics(Resource):

    @jwt_required
    def get(self):

        admin_id = get_jwt_identity()
        admin = AdminModel.find_by_id(admin_id)

        print(admin.__tablename__)

        if admin.__tablename__ != "admin":
            return {'message': 'Not an admin'}

        try:
            no_users = UserModel.find_count()
            no_companies = CompanyModel.find_count()
            no_jobs = JobsModel.find_count()
            no_applications = ApplicationsModel.find_count()
            users = [user.json_for_admin() for user in UserModel.find_all()]
            companies = [company.json_for_admin() for company in CompanyModel.find_all()]

            return {'users': no_users, 'companies': no_companies, 'jobs': no_jobs, 'applications': no_applications, 'users_data': users, "companies_data": companies}

        except:
            return {'message': 'Error'}, 500


# class AdminData(Resource):

#     @jwt_required
#     def get(self):

#         id = get_jwt_identity()

#         admin = UserModel.find_by_id(id)

#         if not admin:
#             return {'message': 'No such admin'}, 401

#         if admin.status != 3:
#             return {'message': 'Not an admin'}, 401

#         try:
#             no_users = UserModel.find_count()
#             no_companies = CompanyModel.find_count()
#             no_jobs = JobsModel.find_count()
#             no_applications = ApplicationsModel.find_count()

#             return {'users': no_users, 'companies': no_companies, 'jobs': no_jobs, 'applications': no_applications}

#         except:
#             return {'message': 'Error'}, 500
