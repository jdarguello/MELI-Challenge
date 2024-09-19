from src.domain.entities.scope import Scope
from sqlalchemy.orm.exc import NoResultFound
from src.root import db

class ScopeService:
    def create(self, name, description):
        new_scope = Scope(name=name, description=description)
        db.session.add(new_scope)
        db.session.commit()
        return new_scope
    
    def get(self, scopeId):
        return db.session.query(Scope).filter_by(scopeId=scopeId).first()
    
    def update(self, scopeId, new_name=None, new_description=None):
        scope = self.get(scopeId)
        scope.name = new_name if new_name is not None else scope.name
        scope.description = new_description if new_description is not None else scope.description
        db.session.commit()
        return scope

    def delete(self, scopeId):
        scope = self.get(scopeId)
        if scope is None:
            raise NoResultFound("Scope with scopeId=" + str(scopeId) + " not found")
        db.session.delete(scope)