from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
import random
import requests
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_refresh_token_required, get_jwt_identity, jwt_required, get_raw_jwt

from models.subscriptions import SubscriptionsModel


class newSubscription(Resource):
    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('plan',
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                            )
        parser.add_argument('start_date',
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                            )
        parser.add_argument('end_date',
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                            )
        parser.add_argument('amount',
                            type=float,
                            required=True,
                            help="This field cannot be blank."
                            )
        parser.add_argument('subscriber_type',
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                            )
        data = parser.parse_args()
        user_id = get_jwt_identity()
        if SubscriptionsModel.find_one(user_id, data['subscriber_type']):
            if SubscriptionsModel.find_one(user_id, data['subscriber_type']).active:
                return {'message': "Already subscribed to an active plan."}, 400

        data['user_id'] = user_id
        subscription = SubscriptionsModel(**data)
        subscription.save_to_db()

        return {'message': 'Subscribed successfuly'}


class Subscription(Resource):
    @jwt_required
    def get(self, id):
        subscription = SubscriptionsModel.find_by_id(id)
        if not subscription:
            return {'message': 'Subscription not found!'}, 401

        return subscription.json(), 200

    @jwt_required
    def delete(self, id):
        subscription = SubscriptionsModel.find_by_id(id)

        if not subscription:
            return {'message': 'Subscription not found.'}, 404
        subscription.delete_from_db()
        return {'message': 'Subscription deleted.'}, 200


class SubscriptionsByIdList(Resource):

    @jwt_required
    def get(self, _type):
        try:
            user_id = get_jwt_identity()
            print(user_id)
            subscriptions = [subscription.json(
            ) for subscription in SubscriptionsModel.find_by_user_id_type(user_id, _type)]

            return {'subscriptions': subscriptions}, 200
        except:
            return {'message': 'Internal server error.'}, 500


class DeactivateS(Resource):

    @jwt_required
    def put(self, id):
        if not SubscriptionsModel.find_by_id(id):
            return {'message': 'Subscription not found.'}, 404

        subscription = SubscriptionsModel.find_by_id(id)

        subscription.active = False
        subscription.save_to_db()

        return {'message': 'Subscription expired.'}, 200
