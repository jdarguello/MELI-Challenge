from src.domain.entities.user import User
from src.application.usecases.role_service import RoleService
from src.application.usecases.identity_provider_service import IdentityProviderService
from sqlalchemy.orm.exc import NoResultFound
from datetime import datetime
from src.root import db

class UserService:
    def __init__(self):
        self.role_service = RoleService()
        self.identity_provider_service = IdentityProviderService()
    
    def temporal_user(self, username, token, identity_provider_id):
        return User(username=username,
            token=token,
            identityProviderId=identity_provider_id)

    def create(self, username, token, identity_provider_id):
        new_user = User(username=username,
            token=token,
            tokenExpiryStart=datetime.now(),
            identity_provider=self.identity_provider_service.get_by_id(identity_provider_id))
        return self.create_by_user(new_user)
    
    def create_by_user(self, user):
        db.session.add(user)
        db.session.commit()
        return user

    def get_by_id(self, user_id):
        user = db.session.query(User).filter_by(userId=user_id).first()
        self._not_found_error(user, user_id)
        return user
    
    def get_by_username(self, username):
        user = db.session.query(User).filter_by(username=username).first()
        self._not_found_error(user, username=username)
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
    
    def get_roles(self, username):
        user = self.get_by_username(username)
        return user.roles
    
    def has_role(self, user, role):
        return role in user.roles

    def update(self, user_id, email=None, token=None):
        user = self.get_by_id(user_id)
        for attr in [("email", email), ("token", token)]:
            if attr[1] is not None:
                setattr(user, attr[0], attr[1])
        db.session.commit()
        return user

    def update_or_create(self, username, token, identity_provider_id):
        try:
            user = self.get_by_username(username)
        except NoResultFound:
            user = None
        if user is None:
            return self.create(username, token, identity_provider_id)
        return self.update(user.userId, token=token)

    def delete(self, user_id):
        user = self.get_by_id(user_id)
        self._not_found_error(user, user_id)
        db.session.delete(user)
    
    def _not_found_error(self, user, user_id=None, username=None):
        if user is None and user_id is not None:
            raise NoResultFound("User with userId=" + str(user_id) + " not found")
        elif user is None and username is not None:
            raise NoResultFound("User with username=" + username + " not found")
        elif user is None:
            raise NoResultFound("User not found. userId=" + str(user_id) + ", username=" + username)