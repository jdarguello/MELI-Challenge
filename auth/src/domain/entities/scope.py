from src.root import db
from src.domain.entities.role import Role

class Scope(db.Model):
    scopeId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))  
    description = db.Column(db.Text)

    # One-to-many relationship with Role
    roles = db.relationship('Role', back_populates='scope', cascade="all, delete-orphan", lazy='select')