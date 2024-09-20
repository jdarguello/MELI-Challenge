from src.domain.entities.type import Type
from src.application.usecases.permissionService import PermissionService
from sqlalchemy.orm.exc import NoResultFound
from src.root import db

class TypeService:
    def __init__(self):
        self.permission_service = PermissionService()

    def create(self, *kind_permissions, **type_attributes):
        new_type = Type(**type_attributes)
        self._set_permissions(new_type, *kind_permissions)
        db.session.add(new_type)
        db.session.commit()
        return new_type
    
    def get(self, type_id):
        type_obj = db.session.query(Type).filter_by(typeId=type_id).first()
        self._not_found_error(type_obj, type_id)
        return type_obj
    
    def update(self, type_id, *kind_permissions, **new_type_attributes):
        type_obj = self.get(type_id)
        self._set_permissions(type_obj, *kind_permissions)
        [setattr(type_obj, key, value) for key, value in new_type_attributes.items() if not self._no_attribute_error(type_obj, key)]
        db.session.commit()
        return type_obj
    
    def remove_permission(self, type_id, kind_permission):
        type_obj = self.get(type_id)
        permission_to_remove = None
        for permission in type_obj.permissions:
            if permission.kind == kind_permission:
                permission_to_remove = permission
                break
        if permission_to_remove is not None:
            type_obj.permissions.remove(permission_to_remove)
        db.session.commit()
        return type_obj

    def delete(self, type_id):
        type_obj = self.get(type_id)
        self._not_found_error(type_obj, type_id)
        db.session.delete(type_obj)
    
    def permission_exists(self, type_obj, kind_permission):
        for permission in type_obj.permissions:
            if permission.kind == kind_permission:
                return True
        return False
    
    def _obj_session(self, obj):
        if not db.session.object_session(obj):
            db.session.add(obj)
    
    def _set_permissions(self, type_obj, *kind_permissions):
        for kind in kind_permissions:
            type_obj.permissions.append(self.permission_service.get(kind))
    
    def _not_found_error(self, type_obj, type_id):
        if type_obj is None:
            raise NoResultFound("Type with typeId=" + str(type_id) + " not found")
    
    def _no_attribute_error(self, type_obj, attribute):
        try:
            getattr(type_obj, attribute)
        except AttributeError:
            raise AttributeError("Type object has no attribute:'" + attribute + "'")
