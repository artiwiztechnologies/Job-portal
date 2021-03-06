from flask import Flask, jsonify, request
from flask import render_template
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from db import db
from blacklist import BLACKLIST
from resources.company import CompanyRegister, Company, CompanyLogin, CompanyTokenRefresh, CompanyLogout, companyemailVerification, CompanyPhoto, getCompanyPhoto, resendCompanyEmail, ForgotCompanyPassword, ResetCompanyPassword, getCompanyCount, getJobsNames, CheckCompany, Applicants
from resources.user import UserRegister, User, UserLogin, TokenRefresh, UserLogout, emailVerification, UserPhoto, getUserPhoto, Resume, getResume, resendEmail, ExpireUser, ForgotUserPassword, ResetUserPassword, getUserFavorites, CheckUser
from resources.jobs import addJob, Job, JobsList, companyJobs, getAppliedJobs, getAppliedUsers, getJobCount
from resources.applications import newApplication, Application, ByJobID, ByUserID, RejectApplication
from resources.favorites import newFavorite, Favorite, getFavorites
from resources.plans import Plan, PlansList, newPlan
from resources.subscriptions import newSubscription, Subscription, SubscriptionsByIdList, DeactivateS
# from resources.orders import newOrderOld, OrdersList, FreeTrial
# from resources.payPayments import newPayment, PaymentsList
from resources.admin import newAdmin, AdminLogin, SendMetrics, getUnapprovedUsers, getUnapprovedCompanies, ApproveUser, ApproveCompany
from resources.support import newSupport
from resources.questions import newQuestion, Question, QuestionsList, PostedQuestions
from resources.comments import newComment
# from resources.payOrders import NewOrder, freeTrial, ordersList
from resources.products import newProduct, ProductPhoto, ProductList, CompanyProductList, ToggleProduct, AdminToggle, ViewProductList, Product
from resources.blogs import newBlog, BlogPhoto, AllBlogs, Blog
from resources.paytmOrders import NewOrder, freeTrial, ordersList
from resources.paytmPayments import newPayment, PaymentsList
from resources.blogComments import newBlogComment

app = Flask(__name__)
CORS(app)

# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://dev:show-password@textile-jobs-do-user-9768146-0.b.db.ondigitalocean.com:25060/production?sslmode=require"
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


# admin

api.add_resource(newAdmin, '/admin-register')
api.add_resource(AdminLogin, '/admin-login')
api.add_resource(SendMetrics, "/admin-data")
api.add_resource(getUnapprovedUsers, "/unapproved-users")
api.add_resource(getUnapprovedCompanies, "/unapproved-companies")
api.add_resource(ApproveUser, "/approve-user/<int:id>")
api.add_resource(ApproveCompany, "/approve-company/<int:id>")

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
api.add_resource(CheckUser, '/check/<string:user_type>')

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
# api.add_resource(ExpireCompany, '/company/check-expiration')
api.add_resource(ForgotCompanyPassword, '/company/forgot-password')
api.add_resource(ResetCompanyPassword, '/company/reset-password')
api.add_resource(getCompanyCount, '/no-of-companies')
api.add_resource(getJobsNames, '/job-titles')
api.add_resource(CheckCompany, '/check-company')
api.add_resource(Applicants, '/applicants')


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
api.add_resource(RejectApplication, '/reject-application/<int:id>')

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
# api.add_resource(newOrderOld, '/new-order')
# api.add_resource(OrdersList, '/orders-list')
# api.add_resource(FreeTrial, '/free-trial')

# payment
# api.add_resource(newPayment, '/new-payment')
# api.add_resource(PaymentsList, '/payments-list')

# support
api.add_resource(newSupport, '/raise-issue')

# questions
api.add_resource(newQuestion, '/post-question')
api.add_resource(Question, '/question/<int:id>')
api.add_resource(QuestionsList, '/question-list')
api.add_resource(PostedQuestions, '/posted-questions/<string:user_type>')

# comments

api.add_resource(newComment, '/post-comment')


# PAYTM
# orders
api.add_resource(NewOrder, '/newOrder')
api.add_resource(freeTrial, '/freeTrial')
api.add_resource(ordersList, '/ordersList')

# payments
api.add_resource(newPayment, '/newPayment')
api.add_resource(PaymentsList, '/paymentsList')

# products
api.add_resource(newProduct, '/new-product')
api.add_resource(Product, '/product/<int:id>')
api.add_resource(ProductPhoto, '/product-picture/<string:path>')
api.add_resource(ProductList, '/product-list')
api.add_resource(ViewProductList, '/view-products')
api.add_resource(CompanyProductList, '/company-products')
api.add_resource(ToggleProduct, '/toggle-product/<int:product_id>')
api.add_resource(AdminToggle, '/admin-toggle/<int:cid>/<int:product_id>')

# blogs
api.add_resource(newBlog, '/new-blog')
api.add_resource(BlogPhoto, '/blog-picture/<string:path>')
api.add_resource(AllBlogs, '/blogs')
api.add_resource(Blog, '/blog/<int:id>')

# blog-comments

api.add_resource(newBlogComment, '/post-blog-comment')

class demo(Resource):
    
    def post(self):

        # parser = reqparse.RequestParser()

        data = request.values

        return jsonify(data)

api.add_resource(demo, '/hook/py')




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
