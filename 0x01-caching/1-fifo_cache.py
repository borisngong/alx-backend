#!/usr/bin/env python3
""" """
from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """ FIFO catching systems """
    def __init__(self):
        """Initialize"""
        super().__init__()
        self.order = []

    def put(self, key, item):
        """Add an item in the cache"""
        if key is None or item is None:
            return

        # Add item to the cache and update order list
        if key not in self.cache_data:
            self.order.append(key)
        self.cache_data[key] = item

        # Next we check if we can replace the item base on FIFO
        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            first_key, _ = self.cache_data.popitem(False)
            print("DISCARD:", first_key)

    def get(self, key):
        if key is None:
            return None
        return self.cache_data.get(key)
