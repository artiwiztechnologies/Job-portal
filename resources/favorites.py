from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
import random
import requests
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_refresh_token_required, get_jwt_identity, jwt_required, get_raw_jwt

from models.favorites import FavoritesModel
from models.user import UserModel
from models.jobs import JobsModel


class newFavorite(Resource):
    @jwt_required
    def post(self, job_id):

        if not JobsModel.find_by_id(job_id):
            return {'message': "Job not found"}, 404
        data = {}
        data['user_id'] = get_jwt_identity()

        if FavoritesModel.find_by_job_user(job_id, data['user_id']):
            return {'message': 'Already added to favorites!'}, 400
        else:
            data['user_email'] = UserModel.find_by_id(data['user_id']).email
            data['job_id'] = job_id
            favorite = FavoritesModel(**data)
            favorite.save_to_db()

            return {'message': 'Applied successfuly!!'}, 200


class Favorite(Resource):

    @jwt_required
    def get(self, id):
        favorite = FavoritesModel.find_by_id(id)
        if not favorite:
            return {'message': 'Job not added to favorites yet!'}, 404
        return favorite.json(), 200

    @jwt_required
    def delete(self, id):
        favorite = FavoritesModel.find_by_id(id)
        if not favorite:
            return {'message': 'Job not added to favorites yet!'}, 404
        favorite.delete_from_db()
        return {'message': 'Removed from favorites!'}, 200


class getFavorites(Resource):
    @jwt_required
    def get(self):
        user_id = get_jwt_identity()
        try:
            favorites = [favorite.json()
                         for favorite in FavoritesModel.find_by_user_id(user_id)]
            if not favorites:
                return {'message': 'No jobs has been added to favorites!'}, 200
            return {'Favorites': favorites, 'message': 'Jobs saved by this user.'}, 200
        except:
            return {'message': 'Error'}, 500
