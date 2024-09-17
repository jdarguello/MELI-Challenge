from src.root import db

class User(db.Model):
    userId = db.Column(db.Integer, primary_key=True)