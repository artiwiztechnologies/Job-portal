from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
import random
import requests
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_refresh_token_required, get_jwt_identity, jwt_required, get_raw_jwt

from models.applications import ApplicationsModel
from models.user import UserModel
from models.jobs import JobsModel

class newApplication(Resource):
    @jwt_required
    def post(self, job_id):

        if not JobsModel.find_by_id(job_id): 
            return {'message': "Job not found."}, 404   
        data = {}
        data['user_id'] = get_jwt_identity()
        # if ApplicationsModel.find_by_user_id_one(data['user_id']) and ApplicationsModel.find_by_job_id_one(job_id) and (ApplicationsModel.find_by_user_id_one(data['user_id']).id is ApplicationsModel.find_by_job_id_one(job_id).id):
        if ApplicationsModel.find_by_job_user(job_id, data['user_id']):    
            return {'message': 'Already applied to this job!'}, 400
        else:
            data['user_email'] = UserModel.find_by_id(data['user_id']).email
            data['job_id'] = job_id
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
            applications = [application.json() for application in ApplicationsModel.find_by_job_id(job_id)]
            if not applications:
                return {'message': 'No applications for this job.'}, 200
            return {'Applications': applications, 'message': 'Users applied to this job.'}, 200
        except:
            return {'message': 'Error'}, 500

class ByUserID(Resource): 

    @jwt_required
    def get(self, user_id):
        try:
            applications = [application.json() for application in ApplicationsModel.find_by_user_id(user_id)]
            if not applications:
                return {'message': 'User has not applied to any jobs.'}, 200
            return {'Applications': applications, 'message': 'Jobs applied by this user.'}, 200
        except:
            return {'message': 'Error'}, 500