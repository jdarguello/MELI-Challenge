import redis

class CacheAdapter:
    def __init__(self, cache):
        self.cache = cache

    def setUser(self, key, value):
        self.cache.set(key, value)

    def getUser(self, email):
        return self.cache.get(email)