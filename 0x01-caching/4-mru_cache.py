#!/usr/bin/env python3
""" Module for working with MRU Cache """
from base_caching import BaseCaching
from collections import OrderedDict


class MRUCache(BaseCaching):
    def __init__(self):
        super().__init__()
        self.cache_data = OrderedDict()
    def put(self, key, item):
        """Add item to cache"""
        if key is None and item is None:
            return
    
        if key in self.cache_data:
            self.cache_data.pop(key)
        

        if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            mru_key, _ = self.cache_data.popitem(last=True)
            print(f"DISCARD: {mru_key}")
        
        # Add new as reccently used
        self.cache_data[key] = item

    def get(self, key):
        """ Retrieves cache"""
        if key is None or key  not in self.cache_data:
            return None
        
        # Move acceseed item to end to make as most recently used
        value = self.cache_data.pop(key)
        self.cache_data[key] = value
        return value