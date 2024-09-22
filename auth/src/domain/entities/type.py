from src.root import db
from src.domain.entities.role import Role
from src.domain.entities.permission import Permission
from src.domain.entities.type_permission import type_permission

class Type(db.Model):
    typeId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)  
    description = db.Column(db.Text, nullable=False)  
    weight = db.Column(db.Integer, default=1)  

    # One-to-many relationship with Role
    roles = db.relationship('Role', back_populates='type', cascade="all, delete-orphan", lazy="select")

    # Many-to-many relationship with Permission
    permissions = db.relationship(
        'Permission', 
        secondary=type_permission, 
    )

    def to_dict(self):
        return {
            "typeId": self.typeId,
            "name": self.name,
            "description": self.description,
            "weight": self.weight,
            "permissions": [permission.to_dict() for permission in self.permissions]
        }

    @classmethod
    def from_dict(cls, data):
        permissions_raw = data.pop("permissions")
        return cls(**data, permissions=[Permission.from_dict(permission) for permission in permissions_raw])

Role.type_from_dict = classmethod(lambda cls, data: Type.from_dict(data))