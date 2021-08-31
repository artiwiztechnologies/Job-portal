# from flask_restful import Resource, reqparse
# from werkzeug.security import safe_str_cmp
# import random
# import requests
# from flask_jwt_extended import create_access_token, create_refresh_token, jwt_refresh_token_required, get_jwt_identity, jwt_required, get_raw_jwt

# from models.jobs import JobsModel
# from blacklist import BLACKLIST

# class addJob(Resource):
#     def post(self):
#         parser = reqparse.RequestParser()

#         parser.add_argument('title',
#                             type=str,
#                             required=True,
#                             help="This field cannot be blank."
#                             )
#         parser.add_argument('Comapny_id',
#                             type=int,
#                             required=True,
#                             help="This field cannot be blank."
#                             )
#         parser.add_argument('description',
#                             type=str,
#                             required=True,
#                             help="This field cannot be blank."
#                             )
#         parser.add_argument('applicants',
#                             type=str,
#                             required=True,
#                             help="This field cannot be blank."
#                             )
#         parser.add_argument('available',
#                             type=bool,
#                             required=True,
#                             help="This field cannot be blank."
#                             )
        
#         data = parser.parse_args()
        
#         if JobsModel.find_by_title(data['title']):
#             return {'message': '{} job already exists'.format(data['title'])}, 400
#         else:
#             job = JobsModel(**data)
#             job.save_to_db()

#             return {'message': 'Job posted successfuly!'}, 201

# class Job(Resource):
#     @jwt_required
#     def get(self, id):
#         job = JobsModel.find_by_id(id)
#         if not job:
#             return {'message': 'Job not found!'}, 404

#         job.delete_from_db()
#         return {'message': 'Job removed!'}, 200

#     @jwt_required
#     def put(self, id):
#         parser = reqparse.RequestParser()

#         parser.add_argument('title',
#                             type=str,
#                             required=True,
#                             help="This field cannot be blank."
#                             )
#         parser.add_argument('Comapny_id',
#                             type=int,
#                             required=True,
#                             help="This field cannot be blank."
#                             )
#         parser.add_argument('description',
#                             type=str,
#                             required=True,
#                             help="This field cannot be blank."
#                             )
#         parser.add_argument('applicants',
#                             type=str,
#                             required=True,
#                             help="This field cannot be blank."
#                             )
#         parser.add_argument('available',
#                             type=bool,
#                             required=True,
#                             help="This field cannot be blank."
#                             )
        
#         data = parser.parse_args()

