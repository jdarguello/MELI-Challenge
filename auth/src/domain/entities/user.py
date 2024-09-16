from src.root import *

class User(db.Model):
    userId = db.Column(db.Integer, primary_key=True)