from run import db
from passlib.hash import pbkdf2_sha256 as sha256

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(120), unique = True, nullable = False)
    password = db.Column(db.String(120), nullable = False)
    content = db.relationship('ContentModel', backref='user')

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def return_all_post(y):
        def to_json_post(x):
            return {
                'text' : x.text,
                'user' : x.user_id
            }
        return list(map(lambda x: to_json_post(x), ContentModel.query.filter_by(user_id = y.id).all()))

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username = username).first()

    @classmethod
    def return_all(cls):
        def to_json(x):
            return {
                'username' : x.username,
                'password' : x.password,
                'contents' : UserModel.return_all_post(x)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
            }
        return {'users' : list(map(lambda x: to_json(x), UserModel.query.all()))}

    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message' : '{} row(s) deleted!'.format(num_rows_deleted)}
        except:
            return {'message' : 'Something went wrong'}

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)

class ContentModel(db.Model):
    __tablename__ = 'contents'

    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.String(120))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, my_id):
        return cls.query.filter_by(id = my_id).first()

    @classmethod
    def return_all(cls):
        def to_json(x):
            return {
                'text' : x.text,
                'user' : x.user_id,
            }
        return {'contents' : list(map(lambda x: to_json(x), ContentModel.query.all()))}

    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message' : '{} row(s) deleted!'.format(num_rows_deleted)}
        except:
            return {'message' : 'Something went wrong'}

class RevokedTokenModel(db.Model):
    __tablename__ = 'revoked_tokens'

    id = db.Column(db.Integer, primary_key = True)
    jti = db.Column(db.String(120))

    def add(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def is_jti_blaklisted(cls, jti):
        query = cls.query.filter_by(jti = jti).first()
        return bool(query)

