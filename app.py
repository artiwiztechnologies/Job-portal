from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from db import db
from blacklist import BLACKLIST
from resources.company import CompanyRegister, Company, CompanyLogin, CompanyTokenRefresh, CompanyLogout
from resources.user import UserRegister, User, UserLogin, TokenRefresh, UserLogout


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



api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:id>')
api.add_resource(UserLogin, '/login')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(UserLogout, '/logout')

api.add_resource(CompanyRegister, '/companyregister')
api.add_resource(Company, '/company/<int:id>')
api.add_resource(CompanyLogin, '/companylogin')
api.add_resource(CompanyTokenRefresh, '/companyrefresh')
api.add_resource(CompanyLogout, '/companylogout')

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