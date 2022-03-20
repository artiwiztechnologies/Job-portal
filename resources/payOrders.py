from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_refresh_token_required, get_jwt_identity, jwt_required, get_raw_jwt
from random import randrange

import requests
import json
from models.orders import OrdersModel
from models.plans import PlansModel
from models.user import UserModel
from models.company import CompanyModel
from models.admin import AdminModel

# import checksum generation utility
# You can get this utility from https://developer.paytm.com/docs/checksum/
from paytmchecksum import PaytmChecksum 

# mid = "mlpZrq88573078670457"
# key = "b0z4TdXl#Az7GxIA"

# PRODUCTION
mid = "fLioeq85351493665452"
key = "uqBbUrOfGQyXVqRE"

class NewOrder(Resource):

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
        parser.add_argument('root',
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                            )
        parser.add_argument('user_type',
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                            )
        
        data = parser.parse_args()


        plan = PlansModel.find_by_id(data['plan_id'])

        jwt_id = get_jwt_identity()

        if not plan:
            return {'message': 'Plan not found.'}, 404

        oid = randrange(1000000000000, 9999999999999)
        while True:
            if not OrdersModel.find_by_id(oid):
                break
            else:
                oid = randrange(1000000000000, 9999999999999)

        data['oid'] = oid

        paytmParams = dict()

        paytmParams["body"] = {
            "requestType"   : "Payment",
            "mid"           : mid,
            "websiteName"   : "DEFAULT",
            "orderId"       : str(oid),
            "callbackUrl"   : "https://api.jobstextile.com/hook/py",
            "txnAmount"     : {
                "value"     : "1.00",
                "currency"  : "INR",
            },
            "userInfo"      : {
                "custId"    : "CUST_1",
            },
        }

        # paytmParams["body"] = {
        #     "requestType"   : "Payment",
        #     "mid"           : mid,
        #     "websiteName"   : "DEFAULT",
        #     "orderId"       : "123456789",
        #     "txnAmount"     : {
        #         "value"     : "199.00",
        #         "currency"  : "INR",
        #     },
        #     "userInfo"      : {
        #         "custId"    : "CUST_09",
        #     },
        # }

        print(paytmParams['body']['orderId'])

        if data['user_type'] == "users":
            cust = UserModel.find_by_id(jwt_id)
        else:
            cust = CompanyModel.find_by_id(jwt_id)

        

        # Generate checksum by parameters we have in body
        # Find your Merchant Key in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys
        checksum = PaytmChecksum.generateSignature(json.dumps(paytmParams["body"]), key)

        paytmParams["head"] = {
            "signature"    : checksum
        }

        post_data = json.dumps(paytmParams)

        # for Staging
        # url = "https://securegw-stage.paytm.in/theia/api/v1/initiateTransaction?mid={}&orderId={}".format(mid, str(oid))

        # for Production
        url = "https://securegw.paytm.in/theia/api/v1/initiateTransaction?mid={}&orderId={}".format(mid, str(oid))

        response = requests.post(url, data = post_data, headers = {"Content-type": "application/json"}).json()
        # print(response)

        # if response['body']['']

        # return response

        data['user_id'] = jwt_id
        data['email'] = cust.email
        data['amount'] = paytmParams['body']['txnAmount']['value']
        data['currency'] = paytmParams['body']['txnAmount']['currency']
        data['status'] = response['body']['resultInfo']['resultMsg']
        data['checksumhash'] = response['head']['signature']

        order = OrdersModel(**data)
        order.save_to_db()
        # return response

        return {'response': {
                'txnToken': response['body']['txnToken'],
                'amount': str(paytmParams['body']['txnAmount']['value']),
                'orderId': str(oid),
                'sig': response['head']['signature'],
                'status': response['body']['resultInfo']['resultMsg']
        }}


class freeTrial(Resource):

    @jwt_required
    def post(self):

        parser = reqparse.RequestParser()

        parser.add_argument('plan_id',
                            type=int,
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


class ordersList(Resource):

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
