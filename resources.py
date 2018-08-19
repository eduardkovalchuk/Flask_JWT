from flask_restful import Resource, reqparse
from models import UserModel, RevokedTokenModel, ContentModel
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt, get_current_user)

parser = reqparse.RequestParser()
parser.add_argument('username', help = 'This field cannot be blank', required = False)
parser.add_argument('password', help = 'This field cannot be blank', required = False)
parser.add_argument('text', help = 'This field cannot be blank', required = False)
parser.add_argument('user', help = 'This field cannot be blank', required = False)

class UserRegistration(Resource):
    def post(self):
        data = parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message' : 'User {} already exists'.format(data['username'])}

        new_user = UserModel(
            username = data['username'],
            password = UserModel.generate_hash(data['password'])
        )
        try:
            new_user.save_to_db()
            access_token = create_access_token(identity = data['username'])
            refresh_token = create_refresh_token(identity = data['username'])
            return {
                'message' : 'User {} was created'.format(data['username']),
                'access_token' : access_token,
                'refresh_token' : refresh_token
                }
        except:
            return {'message' : 'Something went wrong'}, 500

class UserLogin(Resource):
    def post(self):
        data = parser.parse_args()
        current_user = UserModel.find_by_username(data['username'])
        if not current_user:
            return {'message' : 'User {} doesn\'t exist'.format(data['username'])}
        
        if UserModel.verify_hash(data['password'], current_user.password, ):
            access_token = create_access_token(data['username'])
            refresh_token = create_refresh_token(identity = data['username'])
            return {
                'message' : 'Logged in as {}'.format(current_user.username),
                'access_token' : access_token,
                'refresh_token' : refresh_token
            }
        else:
            return {'message' : 'Wrong credentials'}

class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti = jti)
            revoked_token.add()
            return {'message' : 'Access token has been revoked'}
        except:
            return {'message' : 'Something went wrong'}, 500

class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti = jti)
            revoked_token.add()
            return {'message' : 'Refresh token has been revoked'}
        except:
            return {'message' : 'Something went wrong'}, 500

class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity = current_user)
        return {'access-token' : access_token}

class  AllUsers(Resource):
    def get(self):
        return UserModel.return_all()

    def delete(self):
        return UserModel.delete_all()

class OneUser(Resource):
    def get(self, user_id):
        return UserModel.return_one(user_id)
    
    @jwt_required
    def put(self, user_id):
        data = parser.parse_args()
        current_user = get_current_user()
        return {'id' : current_user['id']}
        #UserModel.edit_user(data, user_id)
    
    @jwt_required
    def delete(self, user_id):
        return UserModel.delete_one(user_id)

class AllContents(Resource):
    def get(self):
        return ContentModel.return_all()
    
    @jwt_required
    def delete(self):
        return ContentModel.delete_all()
    
class OneContent(Resource):
    def get(self, content_id):
        return ContentModel.return_one(content_id)
    
    @jwt_required
    def put(self, content_id):
        data = parser.parse_args()
        return ContentModel.edit_content(data, content_id)

    @jwt_required
    def delete(self, content_id):
        return ContentModel.delete_one(content_id)

class ContentAdd(Resource):
    @jwt_required
    def post(self):
        data = parser.parse_args()

        new_post = ContentModel(
            text = data['text'],
            user_id = data['user']
        )
        try:
            new_post.save_to_db()
            return {'message' : 'Post was created'}
        except:
            return {'message' : 'Something went wrong'}, 500


class SecretResource(Resource):
    @jwt_required
    def get(self):
        return{
            'answer' : 42
        }