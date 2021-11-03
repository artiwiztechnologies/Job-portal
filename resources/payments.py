from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from random import randrange
import requests
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_refresh_token_required, get_jwt_identity, jwt_required, get_raw_jwt
import datetime

import hashlib
import hmac

from models.user import UserModel
from models.company import CompanyModel
from models.plans import PlansModel
from models.payments import PaymentsModel
from models.orders import OrdersModel
from models.admin import AdminModel

from dotenv import load_dotenv
import os

load_dotenv()

# key_id = os.getenv('KEY_ID')
# key_secret = os.getenv('KEY_SECRET')

key_id = "rzp_test_V7OA6RGtfz7ILD"
key_secret = "7DQCW16JtDmORBaSxLrwArPh"
# const Razor_pay_key_id = "rzp_test_V7OA6RGtfz7ILD";
# const Razor_pay_key_secret = "7DQCW16JtDmORBaSxLrwArPh";


class newPayment(Resource):

    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('razorpay_payment_id',
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                            )
        parser.add_argument('razorpay_order_id',
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                            )
        parser.add_argument('razorpay_signature',
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                            )
        parser.add_argument('user_type',
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                            )
        parser.add_argument('plan_id',
                            type=int,
                            required=True,
                            help="This field cannot be blank."
                            )

        data = parser.parse_args()

        key_data = data['razorpay_order_id'] + \
            "|" + data['razorpay_payment_id']

        signature_computed = hmac.new(
            key=key_secret.encode('utf-8'),
            msg=key_data.encode('utf-8'),
            digestmod=hashlib.sha256
        ).hexdigest()

        if hmac.compare_digest(data['razorpay_signature'], signature_computed):

            jwt_id = get_jwt_identity()

            plan = PlansModel.find_by_id(data["plan_id"])

            pid = randrange(100000, 999999)
            while True:
                if not PaymentsModel.find_by_pid(pid):
                    break
                else:
                    pid = randrange(100000, 999999)

            # print(oid)

            data['pid'] = pid

            order = OrdersModel.find_by_orderid(data['razorpay_order_id'])
            print(order.oid)
            data['oid'] = order.oid

            if PaymentsModel.find_by_oid(order.oid):
                return {'message': 'Already verified. '}

            if not plan:
                return {'message': 'Plan not available.'}, 404

            if data['user_type'] == "users":
                user = UserModel.find_by_id(jwt_id)

                if not user:
                    return {'message': 'User not found'}, 404

                user.active = True

                date1 = str(datetime.datetime.now()).split(' ')[0][2:]
                date2 = datetime.datetime.strptime(date1, "%y-%m-%d")
                expiry_date = date2 + datetime.timedelta(days=plan.duration)

                user.expiry_date = expiry_date
                user.plan_id = data['plan_id']

                user.save_to_db()

                data['user_id'] = user.id
                data['email'] = user.email
                data['phonenumber'] = user.phonenumber

                payment = PaymentsModel(**data)
                
                payment.save_to_db()

            else:
                company = CompanyModel.find_by_id(jwt_id)

                if not company:
                    return {'message': 'Company not found'}, 404

                company.active = True

                date1 = str(datetime.datetime.now()).split(' ')[0][2:]
                date2 = datetime.datetime.strptime(date1, "%y-%m-%d")
                expiry_date = date2 + datetime.timedelta(days=plan.duration)

                company.expiry_date = expiry_date
                company.plan_id = data['plan_id']

                company.save_to_db()

            return {'message': 'Valid payment.'}, 200
        else:
            return {'message': 'Invalid payment.'}, 400


class PaymentsList(Resource):

    @jwt_required
    def get(self):
        try:
            jwt_id = get_jwt_identity()
            admin = AdminModel.find_by_id(jwt_id)
            if not admin:
                return {'message': 'Not an admin.'}, 401
            if admin.status != 3:
                return {'message': 'Not an admin.'}, 401
            payments = [payment.json() for payment in PaymentsModel.find_all()]

            return {'payments': payments}, 200
        except:
            return {'message': 'Internal server error.'}, 500


# {
#     "razorpay_payment_id": "pay_IAKHt6HcTynKiu",
#     "razorpay_order_id": "order_IAKHXtANe8KwkB",
#     "razorpay_signature": "5ed4bf66615c3468fa0a8eb684571dd14b5e14e146fef613c5ea8e9aed4f5a7e"
# }
