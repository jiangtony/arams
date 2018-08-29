from flask_sqlalchemy import SQLAlchemy
from aram import app

db = SQLAlchemy(app)

class Champion(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    champion_name = db.Column(db.String(120), unique = True)
    champion_id = db.Column(db.Integer, unique = True)
    wins = db.Column(db.Integer)
    losses = db.Column(db.Integer)

    def __init__(self, champion_name, champion_id):
        self.champion_name = champion_name
        self.champion_id = champion_id
        self.wins = 0
        self.losses = 0

    def __repr__(self):
        return f"Champion('{self.champion_name}', '{self.champion_id}', '{self.wins}', '{self.losses}')"


class Ids(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    match_id = db.Column(db.Integer, unique = True)

    def __init__(self, match_id):
        self.match_id = match_id
