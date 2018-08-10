from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from os.path import join, dirname
from dotenv import load_dotenv

app = Flask(__name__)

dotenv_path = join(dirname(dirname(__file__)), '.env')
load_dotenv(dotenv_path)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("POSTGRES_DB_URI")
db = SQLAlchemy(app)


from aram import routes
