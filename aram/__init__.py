from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:pass321@localhost/num_collection'
# db = SQLAlchemy(app)
#
# class Data(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     email = db.Column(db.String(120), unique = True)
#     number = db.Column(db.Integer)
#
#     def __init__(self, email, num):
#         self.email = email
#         self.number = num

from aram import routes
