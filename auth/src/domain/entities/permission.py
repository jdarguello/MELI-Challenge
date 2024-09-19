from src.root import db
from src.domain.entities.type_permission import type_permission

class Permission(db.Model):
    permissionId = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Ensure this is an Integer
    kind = db.Column(db.String(50), unique=True, nullable=False)

     # Many-to-many relationship with Type
    types = db.relationship(
        'Type', 
        secondary=type_permission, 
        back_populates='permissions',
        lazy="select"
    )