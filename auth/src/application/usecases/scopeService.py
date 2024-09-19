from src.domain.entities.scope import Scope
from sqlalchemy.orm.exc import NoResultFound
from src.root import db

class ScopeService:
    def create(self, name, description):
        new_scope = Scope(name=name, description=description)
        db.session.add(new_scope)
        db.session.commit()
        return new_scope
    
    def get(self, scope_id):
        return db.session.query(Scope).filter_by(scopeId=scope_id).first()
    
    def update(self, scope_id, new_name=None, new_description=None):
        scope = self.get(scope_id)
        scope.name = new_name if new_name is not None else scope.name
        scope.description = new_description if new_description is not None else scope.description
        db.session.commit()
        return scope

    def delete(self, scope_id):
        scope = self.get(scope_id)
        if scope is None:
            raise NoResultFound("Scope with scopeId=" + str(scope_id) + " not found")
        db.session.delete(scope)