from src.root import db
from src.domain.entities.role import Role

class Scope(db.Model):
    scopeId = db.Column("scopeid", db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))  
    description = db.Column(db.Text)

    # One-to-many relationship with Role
    roles = db.relationship('Role', cascade="all, delete-orphan", lazy='noload')

    def to_dict(self):
        return {
            "scopeId": self.scopeId,
            "name": self.name,
            "description": self.description
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(**data)

Role.scope_from_dict = classmethod(lambda cls, data: Scope.from_dict(data))