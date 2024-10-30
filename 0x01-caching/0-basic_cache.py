#!/usr/bin/en python3
"""

"""
from base_caching import BaseCaching
class BasicCache(BaseCaching):
    """ Basic Cache catching system without limit"""
    
    def put(self, key, item):
        """ Add an item in the catche """
        if key is not None and item is not None:
            return
        self.cache_data[key] = item

    def get(self, key):
        """ Retrieves an item from the cache by key"""
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data.get(key)
