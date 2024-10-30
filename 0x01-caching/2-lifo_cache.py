#!/usr/bin/env python3
""" LIFO Cache Implementation """
from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """ LIFO caching system """

    def __init__(self):
        """ Initialize """
        super().__init__()
        self.last_key = None  # Keep track of the last added key

    def put(self, key, item):
        """ Add an item in the cache """
        if key is None or item is None:
            return

        # Add item to the cache and update the last added key
        self.cache_data[key] = item
        if key in self.cache_data:
            self.last_key = key

        # Check if we need to discard the last item added
        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            if self.last_key is not None:
                del self.cache_data[self.last_key]
                print(f"DISCARD: {self.last_key}")
                self.last_key = key

    def get(self, key):
        """ Get an item by key """
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data.get(key)
