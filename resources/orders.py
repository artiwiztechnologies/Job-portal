import razorpay
from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from random import randrange
import requests
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_refresh_token_required, get_jwt_identity, jwt_required, get_raw_jwt

from models.orders import OrdersModel
from models.plans import PlansModel
from models.admin import AdminModel

from dotenv import load_dotenv
import os

load_dotenv()

key_id = os.getenv('KEY_ID')
key_secret = os.getenv('KEY_SECRET')

# key_id = "rzp_test_HG5GAR8YfRNzGa"
# key_secret = "Ua2S11sZlyLFZ1uUs2SrAaJ5"

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

        oid = randrange(100000, 999999)
        while True:
            if not OrdersModel.find_by_id(oid):
                break
            else:
                oid = randrange(100000, 999999)

        print(oid)

        post_data['oid'] = oid

        data = {"amount": plan.plan_rate * 100,
                "currency": "INR", "receipt": "order_rcptid_11"}
        payment = client.order.create(data=data)

        order = OrdersModel(**post_data, **payment)
        order.save_to_db()

        # print(order.json())
        return payment, 200


class OrdersList(Resource):

    @jwt_required
    def get(self):
        try:
            jwt_id = get_jwt_identity()
            if not AdminModel.find_by_id(jwt_id):
                return {'message': 'Not an admin.'}, 401
            orders = [order.json() for order in OrdersModel.find_all()]

            return {'orders': orders}, 200
        except:
            return {'message': 'Internal server error.'}, 500
