from flask import Flask, jsonify
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://bcyeykcr:6883g-4vyUe16cJt0LXAqhE3D3dk9V0m@baasu.db.elephantsql.com:5432/bcyeykcr'
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

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']

import views, models, resources

api.add_resource(views.HelloWorld, '/')
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

