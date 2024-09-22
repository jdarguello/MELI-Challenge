from src.application.usecases.userService import UserService
from src.domain.entities.user import User
from src.root import cache
from datetime import datetime, date
import json

# Objetivo: realizar todas las operaciones con cache en un solo lugar
class CacheService:
    def __init__(self):
        self.user_service = UserService()

    def set_user(self, user_id, user):
        cache.set(user_id, json.dumps(user.to_dict(), default=self._date_serializer))
    
    def get_user(self, user_id):
        user = self._date_deserializer(User.from_dict(json.loads(cache.get(user_id))))
        return user
    
    def _date_serializer(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()  # Convert to ISO format string
        raise TypeError(f"Type {type(obj)} not serializable")
    
    def _date_deserializer(self, obj):
        if hasattr(obj, "tokenExpiryStart"):
            setattr(obj, "tokenExpiryStart", datetime.fromisoformat(getattr(obj, "tokenExpiryStart")))
        return obj

    