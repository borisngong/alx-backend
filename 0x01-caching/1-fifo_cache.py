#!/usr/bin/env python3
"""
First-In First-Out caching module
"""
from collections import OrderedDict

from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """
    FIFO caching system
    """
    def __init__(self):
        """Initializes the cache"""
        super().__init__()
        self.cache_data = OrderedDict()

    def put(self, key, item):
        """
        Add an item to the cache following FIFO strategy
        """
        if key is None or item is None:
            return

        # If the key exists, delete it to maintain the insertion order
        if key in self.cache_data:
            del self.cache_data[key]

        # Add the item to the cache
        self.cache_data[key] = item

        # If cache exceeds the limit, pop the first item
        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            oldest_key, _ = self.cache_data.popitem(False)
            print("DISCARD:", oldest_key)

    def get(self, key):
        """
        Get an item by key
        """
        return self.cache_data.get(key, None)
