from src.domain.entities.user import User
from src.application.usecases.role_service import RoleService
from src.application.usecases.identity_provider_service import IdentityProviderService
from sqlalchemy.orm.exc import NoResultFound
from src.root import db

class UserService:
    def __init__(self):
        self.role_service = RoleService()
        self.identity_provider_service = IdentityProviderService()

    def create(self, email, token, token_expiry_date, identity_provider_id):
        new_user = User(email=email,
            token=token,
            token_expiry_date=token_expiry_date,
            identity_provider=self.identity_provider_service.get_by_id(identity_provider_id))
        db.session.add(new_user)
        db.session.commit()
        return new_user

    def get_by_id(self, user_id):
        user = db.session.query(User).filter_by(userId=user_id).first()
        self._not_found_error(user, user_id)
        return user
    
    def get_by_email(self, email):
        user = db.session.query(User).filter_by(email=email).first()
        self._not_found_error(user, email=email)
        return user
    
    def get_all_by_idp(self, idp_id):
        return db.session.query(User).filter_by(identityProviderId=idp_id).all()
    
    def assign_role(self, user_id, role_id):
        user = self.get_by_id(user_id)
        role = self.role_service.get_by_id(role_id)
        if self.has_role(user, role):
            return user
        user.roles.append(role)
        db.session.commit()
        return user
    
    def remove_role(self, user_id, role_id):
        user = self.get_by_id(user_id)
        role = self.role_service.get_by_id(role_id)
        if not self.has_role(user, role):
            return user
        user.roles.remove(role)
        db.session.commit()
        return user
    
    def has_role(self, user, role):
        return role in user.roles

    def update(self, user_id, email=None, token=None, token_expiry_date=None):
        user = self.get_by_id(user_id)
        for attr in [("email", email), ("token", token), ("token_expiry_date", token_expiry_date)]:
            if attr[1] is not None:
                setattr(user, attr[0], attr[1])
        db.session.commit()
        return user

    def delete(self, user_id):
        user = self.get_by_id(user_id)
        self._not_found_error(user, user_id)
        db.session.delete(user)
    
    def _not_found_error(self, user, user_id=None, email=None):
        if user is None and user_id is not None:
            raise NoResultFound("User with userId=" + str(user_id) + " not found")
        elif user is None and email is not None:
            raise NoResultFound("User with email=" + email + " not found")
        elif user is None:
            raise NoResultFound("User not found. userId=" + str(user_id) + ", email=" + email)