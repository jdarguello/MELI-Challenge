from src.domain.entities.role import Role
from src.application.usecases.type_service import TypeService
from src.application.usecases.scopeService import ScopeService
from sqlalchemy.orm.exc import NoResultFound
from src.root import db

class RoleService:
    def __init__(self):
        self.type_service = TypeService()
        self.scope_service = ScopeService()

    def create(self, name, description, type_id, scope_id):
        new_role = Role(name=name, 
            description=description, 
            type=self.type_service.get(type_id), 
            scope=self.scope_service.get(scope_id))
        db.session.add(new_role)
        db.session.commit()
        return new_role
    
    def get_by_id(self, role_id):
        role = db.session.query(Role).filter_by(roleId=role_id).first()
        self._not_found_error(role, role_id)
        return role
    
    def get_by_scope(self, scope_id):
        return db.session.query(Role).filter_by(scope=self.scope_service.get(scope_id)).all()

    def update(self, role_id, new_name=None, new_description=None):
        role = self.get_by_id(role_id)
        role.name = new_name if new_name is not None else role.name
        role.description = new_description if new_description is not None else role.description
        db.session.commit()
        return role

    def delete(self, role_id):
        role = self.get_by_id(role_id)
        self._not_found_error(role, role_id)
        db.session.delete(role)
    
    def _not_found_error(self, role, role_id):
        if role is None:
            raise NoResultFound("Role with roleId=" + str(role_id) + " not found")