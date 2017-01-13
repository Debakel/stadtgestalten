from django.core import cache
from django.core.cache.backends import base


class ProxyCache(base.BaseCache):
    def __init__(self, location, params):
        super().__init__(params)
        self.cache = cache.caches['proxy']

    def get(self, key, default=None, version=None):
        return self.cache.get(key, default=default, version=version)

    def set(self, key, value, timeout=None, version=None):
        return self.cache.set(key, value, timeout=timeout, version=version)

    def delete(self, key):
        return self.cache.delete(key)

    def clear(self):
        return self.cache.clear()