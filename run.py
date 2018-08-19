from flask import Flask, jsonify
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'some-secret-string'

db = SQLAlchemy(app)

@app.before_first_request
def create_tables():
    db.create_all()

app.config['JWT_SECRET_KEY'] = 'jwt-secret-key'
jwt = JWTManager(app)

app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

"""
@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.username

def user_loader(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        username = get_jwt_identity()
        user = UserObject(username=username)
        if not user:
            # This is where you would handle the error case of a user not loading
            return jsonify({"msg": "user not found"}), 404

        # Store the user so you can use it in your endpoints
        g.user = user
        return fn(*args, **kwargs)
    return wrapper


@jwt.user_loader_callback_loader
def custom_user_loader_error(identity):
    ret = {
        'msg' : 'User {} not found'.format(identity)
    }
    return jsonify(ret), 404
"""

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']

import views, models, resources

api.add_resource(resources.UserRegistration, '/registration')
api.add_resource(resources.UserLogin, '/login')
api.add_resource(resources.UserLogoutAccess, '/logout/access')
api.add_resource(resources.UserLogoutRefresh, '/logout/refresh')
api.add_resource(resources.TokenRefresh, '/token/refresh')
api.add_resource(resources.AllUsers, '/users')
api.add_resource(resources.OneUser, '/users/<user_id>')
api.add_resource(resources.AllContents, '/contents')
api.add_resource(resources.OneContent, '/contents/<content_id>')
api.add_resource(resources.ContentAdd, '/contents/add')
api.add_resource(resources.SecretResource, '/secret')
