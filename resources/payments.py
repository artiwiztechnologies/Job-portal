from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
import random
import requests
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_refresh_token_required, get_jwt_identity, jwt_required, get_raw_jwt
import datetime

import hashlib
import hmac

from models.user import UserModel
from models.company import CompanyModel
from models.plans import PlansModel

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
        parser.add_argument('type',
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
        # signature = '5ed4bf66615c3468fa0a8eb684571dd14b5e14e146fef613c5ea8e9aed4f5a7e'
        signature_computed = hmac.new(
            key=key_secret.encode('utf-8'),
            msg=key_data.encode('utf-8'),
            digestmod=hashlib.sha256
        ).hexdigest()
        print(signature_computed)
        print(data['razorpay_signature'])
        if hmac.compare_digest(data['razorpay_signature'], signature_computed):

            jwt_id = get_jwt_identity()

            plan = PlansModel.find_by_id(data["plan_id"])

            if not plan:
                return {'message': 'Plan not available.'}, 404

            if data['type'] == "users":
                user = UserModel.find_by_id(jwt_id)
                user.active = True

                date1 = str(datetime.datetime.now()).split(' ')[0][2:]
                date2 = datetime.datetime.strptime(date1, "%y-%m-%d")
                expiry_date = date2 + datetime.timedelta(days=plan.duration)

                user.expiry_date = expiry_date

                user.save_to_db()
            else:
                company = CompanyModel.find_by_id(jwt_id)
                company.active = True

                date1 = str(datetime.datetime.now()).split(' ')[0][2:]
                date2 = datetime.datetime.strptime(date1, "%y-%m-%d")
                expiry_date = date2 + datetime.timedelta(days=plan.duration)

                company.expiry_date = expiry_date

                company.save_to_db()

            return {'message': 'Valid payment.'}, 200
        else:
            return {'message': 'Invalid payment.'}, 400


# {
#     "razorpay_payment_id": "pay_IAKHt6HcTynKiu",
#     "razorpay_order_id": "order_IAKHXtANe8KwkB",
#     "razorpay_signature": "5ed4bf66615c3468fa0a8eb684571dd14b5e14e146fef613c5ea8e9aed4f5a7e"
# }
