from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
import random
import requests
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_refresh_token_required, get_jwt_identity, jwt_required, get_raw_jwt

from models.jobs import JobsModel
from models.applications import ApplicationsModel
from models.user import UserModel
from models.helper import Helper
from blacklist import BLACKLIST


class addJob(Resource):
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
        parser.add_argument('applicants',
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                            )
        parser.add_argument('available',
                            type=bool,
                            required=True,
                            help="This field cannot be blank."
                            )
        parser.add_argument('job_type',
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                            )
        parser.add_argument('salary',
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                            )
        parser.add_argument('career_level',
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                            )
        parser.add_argument('role',
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                            )
        parser.add_argument('skills',
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                            )

        data = parser.parse_args()
        if JobsModel.find_by_title(data['title']):
            return {'message': '{} job already exists'.format(data['title'])}, 400
        else:
            data['company_id'] = get_jwt_identity()
            job = JobsModel(**data)
            job.save_to_db()

            return {'message': 'Job posted successfuly!'}, 201


class Job(Resource):

    @jwt_required
    def get(self, id):
        job = JobsModel.find_by_id(id)
        if not job:
            return {'message': 'Job Not Found'}, 404
        return job.json(), 200

    @jwt_required
    def delete(self, id):
        job = JobsModel.find_by_id(id)
        if not job:
            return {'message': 'Job Not Found'}, 404
        job.delete_from_db()

        Helper.del_applications_by_job(id)
        Helper.del_favorites_by_job(id)

        # applications = [app.json() for app in ApplicationsModel.find_by_job_id(id)]

        return {'message': 'Job deleted.'}, 200

    @jwt_required
    def put(self, id):
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
        parser.add_argument('applicants',
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                            )
        parser.add_argument('available',
                            type=bool,
                            required=True,
                            help="This field cannot be blank."
                            )
        parser.add_argument('job_type',
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                            )
        parser.add_argument('salary',
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                            )
        parser.add_argument('career_level',
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                            )
        parser.add_argument('role',
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                            )
        parser.add_argument('skills',
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                            )

        data = parser.parse_args()
        if not JobsModel.find_by_id(id):
            return {'message': 'Job not found!'}, 404
        job = JobsModel.find_by_id(id)

        job.title = data['title']
        job.description = data['description']
        job.applicants = data['applicants']
        job.available = data['available']
        job.job_type = data['job_type']
        job.salary = data['salary']
        job.career_level = data['career_level']
        job.role = data['role']
        job.skills = data['skills']

        job.save_to_db()

        return {'message': 'Updated successfuly!'}, 200


class JobsList(Resource):
    @jwt_required
    def get(self):
        # try:
        jobs = [job.json() for job in JobsModel.find_all()]
        return {'Jobs': jobs}, 200
        # except:
        #     return {'message': "Error"}, 500


class companyJobs(Resource):
    @jwt_required
    def get(self, id):
        try:
            jobs = [job.json() for job in JobsModel.find_jobs(id)]
            return {'Jobs': jobs}
        except:
            return {'message': "Error"}, 500


class getAppliedJobs(Resource):
    @jwt_required
    def get(self):
        try:
            jobs = []
            user_id = get_jwt_identity()
            applications = ApplicationsModel.find_by_user_id(user_id)
            print(applications)
            for application in applications:
                job = JobsModel.find_by_id(application.job_id)
                count = ApplicationsModel.find_applicants_count(application.job_id)
                jobs.append(job.json1(application, count))
            if not jobs:
                return {'message': 'User has not applied to any jobs!'}, 400
            return {'Jobs': jobs, 'message': 'Jobs applied by user {}'.format(user_id)}, 200
        except:
            return {'message': 'error'}, 500


class getAppliedUsers(Resource):
    @jwt_required
    def get(self, job_id):
        try:
            users = []
            # user_id = get_jwt_identity()
            applications = ApplicationsModel.find_by_job_id(job_id)
            for application in applications:
                user = UserModel.find_by_id(application.user_id)
                users.append(user.json1(application.id))   
            if not users:
                return {'message': 'No user has applied to this job!'}, 400
            return {'users': users, 'message': 'Users applied to job {}'.format(job_id)}, 200
        except:
            return {'message': 'error'}, 500


class getJobCount(Resource):

    def get(self):
        try:
            total = JobsModel.find_count()
            return {"total": total}, 200
        except:
            return {'message': 'Error'}, 500
