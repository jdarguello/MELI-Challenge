from src.root import db
from src.domain.entities.user_role import user_role

class User(db.Model):
    userId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), nullable=False)
    token = db.Column(db.String(255), nullable=False)
    token_expiry_date = db.Column(db.Date, nullable=False)

    # Nullable foreign key to IdentityProvider
    identityProviderId = db.Column(db.Integer, db.ForeignKey('identity_provider.identityProviderId'), nullable=True)

    # Relationship to IdentityProvider
    identity_provider = db.relationship('IdentityProvider', back_populates='users')

    # Many-to-many relationship with Role
    roles = db.relationship(
        'Role',
        secondary=user_role,
        back_populates='users'
    )
