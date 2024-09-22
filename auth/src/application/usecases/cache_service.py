from src.application.usecases.userService import UserService
from src.domain.entities.user import User
from src.root import cache
from datetime import datetime, date
import json

# Objetivo: realizar todas las operaciones con cache en un solo lugar
class CacheService:
    def __init__(self):
        self.user_service = UserService()

    def set_user(self, username, user):
        cache.set(username, json.dumps(user.to_dict(), default=self._date_serializer))
    
    def get_user(self, username):
        user_raw = cache.get(username)
        if user_raw is None:
            return None
        user = self._date_deserializer(User.from_dict(json.loads(user_raw)))
        return user
    
    def _date_serializer(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()  # Convert to ISO format string
        raise TypeError(f"Type {type(obj)} not serializable")
    
    def _date_deserializer(self, obj):
        if hasattr(obj, "tokenExpiryStart"):
            setattr(obj, "tokenExpiryStart", datetime.fromisoformat(getattr(obj, "tokenExpiryStart")))
        return obj

    