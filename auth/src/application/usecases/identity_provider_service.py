from src.domain.services.identity_provider import IdentityProvider
from sqlalchemy.orm.exc import NoResultFound
from src.root import db

class IdentityProviderService:
    def create(self, **kwargs):
        new_idp = IdentityProvider(**kwargs)
        db.session.add(new_idp)
        db.session.commit()
        return new_idp
    
    def get_by_id(self, id):
        return db.session.query(IdentityProvider).filter_by(identityProviderId=id).first()
    
    def get_by_name(self, name):
        return db.session.query(IdentityProvider).filter_by(name=name).first()
    
    def update(self, name, **kwargs):
        idp = self.get_by_name(name)
        self.no_result_found_error(idp, name)
        [setattr(idp, key, value) for key, value in kwargs.items() if not self.no_attribute_error(idp, key)]
        db.session.commit()
        return idp

    def delete(self, name):
        idp = self.get_by_name(name)
        self.no_result_found_error(idp, name)
        db.session.delete(idp)
    
    def no_result_found_error(self, idp, name):
        if idp is None:
            raise NoResultFound("Identity Provider with name '" + name + "' not found")

    def no_attribute_error(self, idp, attribute):
        try:
            getattr(idp, attribute)
        except AttributeError:
            raise AttributeError("Identity Provider object has no attribute of Type:'" + attribute + "'")
            