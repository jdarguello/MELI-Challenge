from src.domain.services.identity_provider import IdentityProvider
from sqlalchemy.orm.exc import NoResultFound
from flask import request, jsonify
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
    
    def register_idp_in_db(self, body, method):
        idp = self.get_by_name(body['name'])
        if method == "POST":
            if idp is not None:
                return {"message": "Identity Provider already exists"}, 400
            idp = self.create(**body)
            return jsoniify(idp.to_dict()), 201
        if method == "PUT":
            message, status_code, valid = self._idp_args_validation(body, idp)
            if not valid:
                return message, status_code
            name = body.pop("name")
            idp = self.update(name, **body)
            return jsonify(idp.to_dict()), 200
        return {"message": "Identity Provider not found"}, 404
    
    def _idp_args_validation(self, body, idp):
        if idp is None:
            return {"message": "Identity Provider not found"}, 404, False
        if "name" not in body:
            return {"message": "Missing name attribute"}, 400, False
        return None, None, True
    
    def no_result_found_error(self, idp, name):
        if idp is None:
            raise NoResultFound("Identity Provider with name '" + name + "' not found")

    def no_attribute_error(self, idp, attribute):
        try:
            getattr(idp, attribute)
        except AttributeError:
            raise AttributeError("Identity Provider object has no attribute of Type:'" + attribute + "'")
            