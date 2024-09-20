from src.root import db
from src.domain.entities.user import User
from src.domain.entities.user_role import user_role

class Role(db.Model):
    roleId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)

    # Foreign key to Type and Scope
    typeId = db.Column(db.Integer, db.ForeignKey('type.typeId'), nullable=False)
    scopeId = db.Column(db.Integer, db.ForeignKey('scope.scopeId'), nullable=False)

    # Relationship to Type and Scope
    type = db.relationship('Type', back_populates='roles')
    scope = db.relationship('Scope', back_populates='roles')

    # Many-to-many relationship with User
    users = db.relationship(
        'User',
        secondary=user_role,
        lazy="noload"
    )
