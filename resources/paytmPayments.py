from flask_restful import Resource, reqparse
from flask import request
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
from models.paytmPayments import PaymentsModel
from models.orders import OrdersModel
from models.admin import AdminModel

from paytmchecksum import PaytmChecksum 

from dotenv import load_dotenv
import os
import json

load_dotenv()

# mid = "mlpZrq88573078670457"
# key = "b0z4TdXl#Az7GxIA"

# PRODUCTION
mid = "fLioeq85351493665452"
key = "uqBbUrOfGQyXVqRE"

class newPayment(Resource):

    @jwt_required
    def post(self):

        post_data = request.values

        DATA = dict()

        for KEY in post_data:
            if KEY != 'CHECKSUMHASH' and KEY != 'plan_id' and KEY != 'user_type':
                DATA[KEY] = post_data[KEY]

        checksumhash = post_data['CHECKSUMHASH']

        valid = PaytmChecksum.verifySignature(DATA, key, checksumhash)


        plan = PlansModel.find_by_id(post_data['plan_id'])

        jwt_id = get_jwt_identity()

        if not plan:
            return {'message': 'Plan not found.'}, 404


        data = dict()


        if valid:

            pid = randrange(1000000000000, 9999999999999)
            while True:
                if not PaymentsModel.find_by_pid(pid):
                    break
                else:
                    pid = randrange(1000000000000, 9999999999999)

            data['pid'] = pid

            order = OrdersModel.find_by_orderid(post_data['ORDERID'])

            if not order:
                return {'message': "Order not found"}
            print(order.order_id)
            data['oid'] = order.order_id

            if PaymentsModel.find_by_oid(order.oid):
                return {'message': 'Already verified. '}

            if not plan:
                return {'message': 'Plan not available.'}, 404

            if post_data['user_type'] == "users":
                user = UserModel.find_by_id(jwt_id)

                if not user:
                    return {'message': 'User not found'}, 404

                user.active = True

                date1 = str(datetime.datetime.now()).split(' ')[0][2:]
                date2 = datetime.datetime.strptime(date1, "%y-%m-%d")
                expiry_date = date2 + datetime.timedelta(days=plan.duration)

                user.expiry_date = expiry_date
                user.plan_id = post_data['plan_id']

                user.save_to_db()

                data['user_id'] = user.id
                data['email'] = user.email
                data['phonenumber'] = user.phonenumber
                data['user_type'] = post_data['user_type']
                data['plan_id'] = post_data["plan_id"]

                payment = PaymentsModel(data['pid'], data['oid'], data['user_id'], data['email'], data['plan_id'], data['phonenumber'], data['user_type'])
                
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
                company.plan_id = post_data['plan_id']

                company.save_to_db()

                data['user_id'] = company.id
                data['email'] = company.email
                data['phonenumber'] = company.phonenumber
                data['user_type'] = post_data['user_type']
                data['plan_id'] = post_data["plan_id"]

                payment = PaymentsModel(data['pid'], data['oid'], data['user_id'], data['email'], data['plan_id'], data['phonenumber'], data['user_type'])
                
                payment.save_to_db()

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


