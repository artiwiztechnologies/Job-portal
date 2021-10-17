import razorpay
from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
import random
import requests
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_refresh_token_required, get_jwt_identity, jwt_required, get_raw_jwt

from models.orders import OrdersModel
from models.plans import PlansModel

key_id = "rzp_test_V7OA6RGtfz7ILD"
key_secret = "7DQCW16JtDmORBaSxLrwArPh"

client = razorpay.Client(
    auth=(key_id, key_secret))


class newOrder(Resource):

    def post(self):

        parser = reqparse.RequestParser()

        parser.add_argument('plan_id',
                            type=int,
                            required=True,
                            help="This field cannot be blank."
                            )
        parser.add_argument('user_id',
                            type=int,
                            required=True,
                            help="This field cannot be blank."
                            )
        parser.add_argument('email',
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                            )
        parser.add_argument('user_type',
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                            )

        post_data = parser.parse_args()

        plan = PlansModel.find_by_id(post_data['plan_id'])

        if not plan:
            return {'message': 'Plan not found.'}, 404

        data = {"amount": plan.plan_rate * 100,
                "currency": "INR", "receipt": "order_rcptid_11"}
        payment = client.order.create(data=data)

        order = OrdersModel(**post_data, **payment)
        order.save_to_db()

        # print(order.json())
        return payment, 200


class OrdersList(Resource):

    def get(self):
        try:
            orders = [order.json() for order in OrdersModel.find_all()]

            return {'orders': orders}, 200
        except:
            return {'message': 'Internal server error.'}, 500
