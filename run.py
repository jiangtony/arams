from aram import app
import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("POSTGRES_DB_URI")
db = SQLAlchemy(app)

class Champion(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    champion_name = db.Column(db.String(120), unique = True)
    champion_id = db.Column(db.Integer)
    wins = db.Column(db.Integer)
    losses = db.Column(db.Integer)

    def __repr__(self):
        return f"Champion('{self.champion_name}', '{self.champion_id}', '{self.wins}', '{self.losses}')"

if __name__ == "__main__":
    app.run(debug=True)
