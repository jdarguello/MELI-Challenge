from src.root import db
from src.domain.entities.user import User
from src.domain.entities.user_role import user_role

class Role(db.Model):
    roleId = db.Column("roleid", db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)

    # Foreign key to Type and Scope
    typeId = db.Column("typeid", db.Integer, db.ForeignKey('type.typeid'), nullable=False)
    scopeId = db.Column("scopeid", db.Integer, db.ForeignKey('scope.scopeid'), nullable=False)

    # Relationship to Type and Scope
    type = db.relationship('Type', back_populates='roles')
    scope = db.relationship('Scope', back_populates='roles')

    # Many-to-many relationship with User
    users = db.relationship(
        'User',
        secondary=user_role,
        lazy="noload"
    )

    def to_dict(self):
        return {
            "roleId": self.roleId,
            "name": self.name,
            "description": self.description,
            "type": self.type.to_dict(),
            "scope": self.scope.to_dict()
        }
    
    @classmethod
    def from_dict(cls, data):
        type = cls.type_from_dict(data.pop("type"))
        scope = cls.scope_from_dict(data.pop("scope"))
        return cls(**data, type=type, scope=scope)

User.role_from_dict = classmethod(lambda cls, data: Role.from_dict(data))