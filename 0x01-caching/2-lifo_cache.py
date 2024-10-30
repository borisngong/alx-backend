#!/usr/bin/env python3
"""Last-In First-Out caching module.
"""
from collections import OrderedDict
from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """
    LIFO caching system
    """
    def __init__(self):
        """Initializes the cache"""
        super().__init__()
        self.cache_data = OrderedDict()

    def put(self, key, item):
        """
        Adds an item in the cache
        """
        if key is None or item is None:
            return

        # Add the item and check for capacity overflow
        self.cache_data[key] = item
        self.cache_data.move_to_end(key, last=True)

        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            last_key, _ = self.cache_data.popitem(last=True)
            print("DISCARD:", last_key)

    def get(self, key):
        """
        Retrieves an item by key
        """
        return self.cache_data.get(key, None)
