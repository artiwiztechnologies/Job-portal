from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
import random
import requests
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_refresh_token_required, get_jwt_identity, jwt_required, get_raw_jwt

from models.plans import PlansModel


class newPlan(Resource):
    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('plan_name',
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                            )
        parser.add_argument('plan_rate',
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                            )
        parser.add_argument('duration',
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                            )

        data = parser.parse_args()
        if PlansModel.find_by_plan_name(data['plan_name']):
            return {'message': "{} plan already exists.".format(data['plan_name'])}, 400
        else:
            plan = PlansModel(**data)
            plan.save_to_db()

            return {'message': 'Plan added successfuly!'}, 200


class Plan(Resource):

    def get(self, id):
        plan = PlansModel.find_by_id(id)
        if not plan:
            return {'message': 'Plan not found!'}, 401

        return plan.json(), 200

    @jwt_required
    def delete(self, id):
        plan = PlansModel.find_by_id(id)

        if not plan:
            return {'message': 'Plan not found.'}, 404
        plan.delete_from_db()
        return {'message': 'Plan deleted.'}, 200

    @jwt_required
    def put(slef, id):
        parser = reqparse.RequestParser()

        parser.add_argument('plan_name',
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                            )
        parser.add_argument('plan_rate',
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                            )
        parser.add_argument('duration',
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                            )

        data = parser.parse_args()
        if not PlansModel.find_by_id(id):
            return {'message': 'Plan not found'}, 404
        plan = PlansModel.find_by_id(id)

        plan.plan_name = data['plan_name']
        plan.plan_rate = data['plan_rate']
        plan.duration = data['duration']

        plan.save_to_db()

        return {'message': 'Updated successfuly'}, 200


class PlansList(Resource):

    def get(self):
        try:
            plans = [plan.json() for plan in PlansModel.find_all()]

            return {'plans': plans}, 200
        except:
            return {'message': 'Internal server error.'}, 500
