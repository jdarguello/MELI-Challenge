from src.root import db

class Type(db.Model):
    typeId = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))  
    description = db.Column(db.Text)  
    weight = db.Column(db.Integer)  