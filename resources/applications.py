from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
import random
import requests
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_refresh_token_required, get_jwt_identity, jwt_required, get_raw_jwt

from models.applications import ApplicationsModel
from models.user import UserModel
from models.jobs import JobsModel
from models.company import CompanyModel


class newApplication(Resource):
    @jwt_required
    def post(self, job_id):

        if not JobsModel.find_by_id(job_id):
            return {'message': "Job not found."}, 404
        data = {}
        data['user_id'] = get_jwt_identity()

        application = ApplicationsModel.find_by_job_user(
            job_id, data['user_id'])

        if application and application.status == "applied":
            return {'message': 'Already applied to this job!'}, 400
        else:
            user = UserModel.find_by_id(data['user_id'])
            data['user_name'] = user.name
            data['user_email'] = user.email
            data['job_id'] = job_id

            job = JobsModel.find_by_id(job_id)
            data['company_id'] = job.company_id

            company = CompanyModel.find_by_id(job.company_id)
            data['company_name'] = company.name

            application = ApplicationsModel(**data)
            application.save_to_db()

            return {'message': 'Applied successfuly!!'}, 200


class Application(Resource):

    @jwt_required
    def get(self, id):
        application = ApplicationsModel.find_by_id(id)
        if not application:
            return {'message': 'Application not found!'}, 404
        return application.json(), 200

    @jwt_required
    def delete(self, id):
        application = ApplicationsModel.find_by_id(id)
        if not application:
            return {'message': 'Application not Found'}, 404
        application.delete_from_db()
        return {'message': 'Application deleted.'}, 200


class ByJobID(Resource):

    @jwt_required
    def get(self, job_id):
        try:
            applications = [application.json()
                            for application in ApplicationsModel.find_by_job_id(job_id)]
            if not applications:
                return {'message': 'No applications for this job.'}, 200
            return {'Applications': applications, 'message': 'Users applied to this job.'}, 200
        except:
            return {'message': 'Error'}, 500


class ByUserID(Resource):

    @jwt_required
    def get(self, user_id):
        try:
            applications = [application.json(
            ) for application in ApplicationsModel.find_by_user_id(user_id)]
            if not applications:
                return {'message': 'User has not applied to any jobs.'}, 200
            return {'Applications': applications, 'message': 'Jobs applied by this user.'}, 200
        except:
            return {'message': 'Error'}, 500


class RejectApplication(Resource):

    @jwt_required
    def get(self, id):

        application = ApplicationsModel.find_by_id(id)

        if not application:
            return {'message': 'Application not found.'}, 404

        if application.status == "rejected":
            return {'message': 'Application already rejected.'}, 400

        user = UserModel.find_by_id(application.user_id)

        if not user:
            return {'message': 'User not found.'}, 404

        job = JobsModel.find_by_id(application.job_id)

        application.send_rejection_email(
            user, job.title, application.company_name)

        application.status = "rejected"
        application.save_to_db()

        return {'message': 'Application rejected.'}, 200


class AcceptApplication(Resource):

    @jwt_required
    def get(self, id):

        application = ApplicationsModel.find_by_id(id)

        if not application:
            return {'message': 'Application not found.'}, 404

        user = UserModel.find_by_id(application.user_id)

        if not user:
            return {'message': 'User not found.'}, 404

        application.send_rejection_email(user)

        application.status = "accepted"
        application.save_to_db()

        return {'message': 'Application accepted.'}, 200


# class CompanyApplicants(Resource):

#     @jwt_required
#     def get(self, company_id):
#         try:
#             if not CompanyModel.find_by_id(company_id):
#                 return {'message': 'Company not founs'}, 404
#             applications_main = [application.json(
#             ) for application in ApplicationsModel.find_by_company_id(company_id)]

#             applications = ApplicationsModel.find_by_company_id(company_id)

#             if not applications:
#                 return {'message': 'No users have applied to this company'}, 401

#             applicants = []
#             for application in applications:
#                 user = UserModel.find_by_id(application.user_id)
#                 applicants.append(user.json1(application.json()))
#             return {'Applicants': applicants}
#         except:
#             return {'message': 'Error'}, 500
