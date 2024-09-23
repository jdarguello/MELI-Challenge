from src.root import db
from src.domain.entities.user_role import user_role
from src.domain.services.identity_provider import IdentityProvider
from datetime import datetime, timedelta

class User(db.Model):
    __tablename__ = 'app_user'
    userId = db.Column("userid", db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), nullable=False)
    token = db.Column(db.String(255), nullable=False)
    tokenExpiryStart = db.Column("tokenexpirystart", db.DateTime, nullable=False)

    # Nullable foreign key to IdentityProvider
    identityProviderId = db.Column("identityproviderid", db.Integer, db.ForeignKey('identity_provider.identityproviderid'), nullable=True)

    # Relationship to IdentityProvider
    identity_provider = db.relationship('IdentityProvider', back_populates='users', lazy='joined')

    # Many-to-many relationship with Role
    roles = db.relationship(
        'Role',
        secondary=user_role,
        back_populates='users'
    )

    def valid_token(self):
        # Debe retornar un booleano, comparando la fecha actual con la token_expiry_start + el tokenExpiryTime (tiempo en segundos)
        return self.tokenExpiryStart + timedelta(seconds=self.identity_provider.tokenExpiryTime) > datetime.now()
    
    def to_dict(self):
        return {
            "userId": self.userId,
            "username": self.username,
            "token": self.token,
            "tokenExpiryStart": self.tokenExpiryStart,
            "identityProvider": self.identity_provider.to_dict(),
            "roles": [role.to_dict() for role in self.roles]
        }
    
    @classmethod
    def from_dict(cls, data):
        identity_provider = IdentityProvider.from_dict(data.pop("identityProvider"))
        roles_raw = data.pop("roles")
        return cls(**data, identity_provider=identity_provider, 
            roles=[cls.role_from_dict(role) for role in roles_raw])
