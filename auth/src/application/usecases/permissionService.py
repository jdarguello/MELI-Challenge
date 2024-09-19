from src.domain.entities.permission import Permission
from sqlalchemy.orm.exc import NoResultFound
from src.root import db

class PermissionService:
    def create(self, kind):
        new_permission = Permission(kind=kind)
        db.session.add(new_permission)
        db.session.commit()
        return new_permission
    
    def get(self, kind):
        return db.session.query(Permission).filter_by(kind=kind).first()
    
    def update(self, kind, new_kind):
        permission = self.get(kind)
        permission.kind = new_kind
        db.session.commit()
        return permission
    
    def delete(self, kind):
        permission = self.get(kind)
        if permission is None:
            raise NoResultFound("Permission '" + kind + "' not found")
        db.session.delete(permission)