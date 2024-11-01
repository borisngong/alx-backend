#!/usr/bin/env python3
"""Module for working with LFU Cache"""
from base_caching import BaseCaching
from collections import OrderedDict, defaultdict


class LFUCache(BaseCaching):
    """ LFU Caching System """
    def __init__(self):
        super().__init__()
        self.cache_data = OrderedDict()
        self.frequency = defaultdict(int)  # To track usage frequency

    def put(self, key, item):
        """Add item to cache"""
        if key is None or item is None:
            return

        # If key is already in cache, update item and increase frequency
        if key in self.cache_data:
            self.cache_data[key] = item
            self.frequency[key] += 1
            self.cache_data.move_to_end(key)  # Mark as recently used
        else:
            # If cache is at max capacity, apply LFU + LRU eviction policy
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                min_freq = min(self.frequency.values())
                l_fu = [k for k, v in self.frequency.items() if v == min_freq]

                for k in self.cache_data:
                    if k in l_fu:
                        self.cache_data.pop(k)
                        self.frequency.pop(k)
                        break

            # Add new key with initial frequency of 1
            self.cache_data[key] = item
            self.frequency[key] = 1
            self.cache_data.move_to_end(key)

    def get(self, key):
        """Get item by key"""
        if key is None or key not in self.cache_data:
            return None

        # Update frequency and mark as recently used
        self.frequency[key] += 1
        self.cache_data.move_to_end(key)
        return self.cache_data[key]
