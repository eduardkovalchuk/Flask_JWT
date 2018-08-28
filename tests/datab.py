from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_data_base.db'
db = SQLAlchemy(app)

class DataBase(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(120), unique = True, nullable = False)
    password = db.Column(db.String(120), nullable = False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    @staticmethod
    def created_database():
        #create table
        db.create_all()

    @staticmethod
    def insert_data(username, password):
        #insert some data

        new_user = DataBase(username, password)
        db.session.add(new_user)
        db.session.commit()

    @staticmethod
    def select_data(user_id):
        #select some data

        result = DataBase.query.filter_by(id=user_id).first()

        return result.username

    @staticmethod
    def drop_database():
        db.drop_all()
