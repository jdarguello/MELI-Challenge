from src.root import db
from src.domain.entities.user_role import user_role
from datetime import datetime, timedelta

class User(db.Model):
    __tablename__ = 'app_user'
    userId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), nullable=False)
    token = db.Column(db.String(255), nullable=False)
    tokenExpiryStart = db.Column(db.Date, nullable=False)

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

    def valid_token(self):
        # Debe retornar un booleano, comparando la fecha actual con la token_expiry_start + el tokenExpiryTime (tiempo en segundos)
        return self.tokenExpiryStart + timedelta(seconds=self.identity_provider.tokenExpiryTime) > datetime.now()
