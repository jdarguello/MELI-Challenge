from src.root import db

class IdentityProvider(db.Model):
    identityProviderId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    clientId = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), unique=True, nullable=False)  
    clientSecret = db.Column(db.String(255), nullable=False)
    baseUrl = db.Column(db.String(255), nullable=False)
    tokenUrl = db.Column(db.String(255), nullable=False)
    authorizationUrl = db.Column(db.String(255), nullable=False)
    redirectUrl = db.Column(db.String(255), nullable=False)

    # One-to-many relationship with User (without cascade)
    users = db.relationship('User', back_populates='identity_provider', lazy='select')
    