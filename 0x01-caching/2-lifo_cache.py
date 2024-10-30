#!/usr/bin/env python3
"""
Module for working with LIFO cache  system
"""
from collections import OrderedDict
from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """
    LIFO cache system with item discarding on overflow
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
        if key not in self.cache_data:
            if len(self.cache_data) + 1 > BaseCaching.MAX_ITEMS:
                in_last_key, _ = self.cache_data.popitem(True)
                print("DISCARD:", in_last_key)
        self.cache_data[key] = item
        self.cache_data.move_to_end(key, last=True)

    def get(self, key):
        """
        Get an item by key
        """
        return self.cache_data.get(key, None)
