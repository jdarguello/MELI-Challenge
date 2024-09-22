from src.root import db

class IdentityProvider(db.Model):
    identityProviderId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    clientId = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), unique=True, nullable=False)  
    clientSecret = db.Column(db.String(255), nullable=False)
    tokenValidationUrl = db.Column(db.String(255), nullable=False)
    tokenExpiryTime = db.Column(db.Integer, nullable=False)     # In seconds

    # One-to-many relationship with User (without cascade)
    users = db.relationship('User', back_populates='identity_provider', lazy='select')

    def to_dict(self):
        return {
            "identityProviderId": self.identityProviderId,
            "clientId": self.clientId,
            "name": self.name,
            "clientSecret": self.clientSecret,
            "tokenValidationUrl": self.tokenValidationUrl,
            "tokenExpiryTime": self.tokenExpiryTime
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(**data)
    