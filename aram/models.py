from aram import db

class Champion(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    champion_name = db.Column(db.String(120), unique = True)
    champion_id = db.Column(db.Integer)
    wins = db.Column(db.Integer)
    losses = db.Column(db.Integer)

    def __repr__(self):
        return f"Champion('{self.champion_name}', '{self.champion_id}', '{self.wins}', '{self.losses}')"
