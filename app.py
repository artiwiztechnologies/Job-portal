from flask import Flask, jsonify
from flask import render_template
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from db import db
from blacklist import BLACKLIST
from resources.company import CompanyRegister, Company, CompanyLogin, CompanyTokenRefresh, CompanyLogout, companyemailVerification, CompanyPhoto, getCompanyPhoto, resendCompanyEmail, ExpireCompany, ForgotCompanyPassword, ResetCompanyPassword, getCompanyCount
from resources.user import UserRegister, User, UserLogin, TokenRefresh, UserLogout, emailVerification, UserPhoto, getUserPhoto, Resume, getResume, resendEmail, ExpireUser, ForgotUserPassword, ResetUserPassword, getUserFavorites
from resources.jobs import addJob, Job, JobsList, companyJobs, getAppliedJobs, getAppliedUsers, getJobCount
from resources.applications import newApplication, Application, ByJobID, ByUserID, CompanyApplicants
from resources.favorites import newFavorite, Favorite, getFavorites
from resources.plans import Plan, PlansList, newPlan
from resources.subscriptions import newSubscription, Subscription, SubscriptionsByIdList, DeactivateS
from resources.orders import newOrder, OrdersList
from resources.payments import newPayment

app = Flask(__name__)
CORS(app)

# app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://karthik:karthikkaran@database-1.c3gbi1q1hlzf.us-east-2.rds.amazonaws.com:5432/otaupdatedb"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True  # enable blacklist feature
# allow blacklisting for access and refresh tokens
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
# UPLOAD_FOLDER = '/Users/karthik/Desktop/Personal_Code/productimages'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.secret_key = 'jose'  # could do app.config['JWT_SECRET_KEY'] if we prefer
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWTManager(app)

"""
`claims` are data we choose to attach to each jwt payload
and for each jwt protected endpoint, we can retrieve these claims via `get_jwt_claims()`
one possible use case for claims are access level control, which is shown below.
"""


@jwt.user_claims_loader
# Remember identity is what we define when creating the access token
def add_claims_to_jwt(identity):
    if identity == 1:   # instead of hard-coding, we should read from a config file or database to get a list of admins instead
        return {'is_admin': True}
    return {'is_admin': False}


# This method will check if a token is blacklisted, and will be called automatically when blacklist is enabled
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    # Here we blacklist particular JWTs that have been created in the past.
    return decrypted_token['jti'] in BLACKLIST


# The following callbacks are used for customizing jwt response/error messages.
# The original ones may not be in a very pretty format (opinionated)
@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'message': 'The token has expired.',
        'error': 'token_expired'
    }), 401


@jwt.invalid_token_loader
# we have to keep the argument here, since it's passed in by the caller internally
def invalid_token_callback(error):
    return jsonify({
        'message': 'Signature verification failed.',
        'error': 'invalid_token'
    }), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        "description": "Request does not contain an access token.",
        'error': 'authorization_required'
    }), 401


@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        "description": "The token is not fresh.",
        'error': 'fresh_token_required'
    }), 401


@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        "description": "The token has been revoked.",
        'error': 'token_revoked'
    }), 401


@app.route("/token-expired")
def token():
    return render_template('token_expired.html')


# user
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:id>')  # delete to be removed later
api.add_resource(UserLogin, '/login')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(UserLogout, '/logout')
api.add_resource(emailVerification, '/confirm-email/<string:token>')
api.add_resource(resendEmail, '/resendemail/<int:id>')
api.add_resource(UserPhoto, '/uploaduserphoto')
api.add_resource(getUserPhoto, '/user/<string:path>')
api.add_resource(Resume, '/user/upload-resume')
api.add_resource(getResume, '/user-resume/<string:path>')
api.add_resource(ExpireUser, '/user/check-expiration')
api.add_resource(ForgotUserPassword, '/user/forgot-password')
api.add_resource(ResetUserPassword, '/user/reset-password')
api.add_resource(getUserFavorites, '/user/favorites')


# company
api.add_resource(CompanyRegister, '/companyregister')
api.add_resource(Company, '/company/<int:id>')
api.add_resource(CompanyLogin, '/companylogin')
api.add_resource(CompanyTokenRefresh, '/companyrefresh')
api.add_resource(CompanyLogout, '/companylogout')
api.add_resource(companyemailVerification,
                 '/companyconfirm-email/<string:token>')
api.add_resource(resendCompanyEmail, '/resendcompanyemail/<int:id>')
api.add_resource(CompanyPhoto, '/uploadcompanyphoto')
api.add_resource(getCompanyPhoto, '/company/<string:path>')
api.add_resource(ExpireCompany, '/company/check-expiration')
api.add_resource(ForgotCompanyPassword, '/company/forgot-password')
api.add_resource(ResetCompanyPassword, '/company/reset-password')
api.add_resource(getCompanyCount, '/no-of-companies')


# jobs
api.add_resource(addJob, '/post-job')
api.add_resource(Job, '/job/<int:id>')
api.add_resource(JobsList, '/jobs-list')
api.add_resource(companyJobs, '/company-jobs/<int:id>')
api.add_resource(getAppliedJobs, '/appliedjobs')
api.add_resource(getAppliedUsers, '/appliedusers/<int:job_id>')
api.add_resource(getJobCount, '/no-of-jobs')

# applications
api.add_resource(newApplication, '/apply/<int:job_id>')
api.add_resource(Application, '/application/<int:id>')
api.add_resource(ByJobID, '/get-users/<int:job_id>')
api.add_resource(ByUserID, '/get-jobs/<int:user_id>')
api.add_resource(CompanyApplicants, '/company-applcants/<int:company_id>')

# favorited
api.add_resource(newFavorite, '/add-favorite/<int:job_id>')
api.add_resource(Favorite, '/favorite/<int:id>')
api.add_resource(getFavorites, '/get-favorites')


# plan
api.add_resource(newPlan, '/add-plan')
api.add_resource(Plan, '/plan/<int:id>')
api.add_resource(PlansList, '/plan-list')


# subscribe
api.add_resource(newSubscription, '/subscribe')
api.add_resource(Subscription, '/subscription/<int:id>')
api.add_resource(SubscriptionsByIdList, '/subscription-list/<string:_type>')
api.add_resource(DeactivateS, '/deactivate/<int:id>')


# order
api.add_resource(newOrder, '/new-order')
api.add_resource(OrdersList, '/orders-list')


# payment
api.add_resource(newPayment, '/new-payment')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5005, debug=True)


# {
#     "phonenumber": "9585570987",
#     "password": "123456"
# }
# {
#      "name": "felix",
#      "phonenumber": "9585570987",
#      "email": "felix@gmail.com",
#      "address": "main road",
#      "password": "123456",
#      "photoURL": "abd/adde/ss",
#      "active": true
#  }
