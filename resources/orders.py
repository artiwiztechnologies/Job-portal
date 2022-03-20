import razorpay
from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from random import randrange
import requests
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_refresh_token_required, get_jwt_identity, jwt_required, get_raw_jwt
import datetime

from models.orders import OrdersModel
from models.plans import PlansModel
from models.admin import AdminModel
from models.user import UserModel
from models.company import CompanyModel

from dotenv import load_dotenv
import os

load_dotenv()

key_id = os.getenv('KEY_ID')
key_secret = os.getenv('KEY_SECRET')

# key_id = "rzp_test_HG5GAR8YfRNzGa"
# key_secret = "Ua2S11sZlyLFZ1uUs2SrAaJ5"

client = razorpay.Client(
    auth=(key_id, key_secret))


class newOrderOld(Resource):

    @jwt_required
    def post(self):

        parser = reqparse.RequestParser()

        parser.add_argument('plan_id',
                            type=int,
                            required=True,
                            help="This field cannot be blank."
                            )
        # parser.add_argument('user_id',
        #                     type=int,
        #                     required=True,
        #                     help="This field cannot be blank."
        #                     )
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

        jwt_id = get_jwt_identity()

        if not plan:
            return {'message': 'Plan not found.'}, 404

        # if plan.trial:
        #     return free_trial(jwt_id, post_data['user_type'], plan)

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


class FreeTrial(Resource):

    @jwt_required
    def post(self):

        parser = reqparse.RequestParser()

        parser.add_argument('plan_id',
                            type=int,
                            required=True,
                            help="This field cannot be blank."
                            )
        # parser.add_argument('user_id',
        #                     type=int,
        #                     required=True,
        #                     help="This field cannot be blank."
        #                     )
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

        jwt_id = get_jwt_identity()

        if not plan:
            return {'message': 'Plan not found.'}, 404

        if not plan.trial:
            return {'message': 'Not a free plan.'}

        if post_data['user_type'] == 'users':
            user = UserModel.find_by_id(jwt_id)
            if user.active:
                return {'message': 'Already subscribed to a plan'}
            elif user.trial_availed:
                return {'message': 'Free trial used already.'}
            else:
                user.trial_availed = True
                user.active = True

                date1 = str(datetime.datetime.now()).split(' ')[0][2:]
                date2 = datetime.datetime.strptime(date1, "%y-%m-%d")
                expiry_date = date2 + \
                    datetime.timedelta(days=plan.duration)

                user.expiry_date = expiry_date
                user.plan_id = plan.id

                user.save_to_db()

                return {'message': 'Subscribed to free trial.'}
        else:
            company = CompanyModel.find_by_id(jwt_id)
            if company.trial_availed:
                return {'message': 'Free trial used already.'}
            elif company.active:
                return {'message': 'Already subscribed to a plan'}
            else:
                company.trial_availed = True
                company.active = True

                date1 = str(datetime.datetime.now()).split(' ')[0][2:]
                date2 = datetime.datetime.strptime(date1, "%y-%m-%d")
                expiry_date = date2 + \
                    datetime.timedelta(days=plan.duration)

                company.expiry_date = expiry_date
                company.plan_id = plan.id

                company.save_to_db()

                return {'message': 'Subscribed to free trial.'}


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
