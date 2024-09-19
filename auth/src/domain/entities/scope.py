from src.root import db

class Scope(db.Model):
    scopeId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))  
    description = db.Column(db.Text)