#!/usr/bin/env python3

from collections import defaultdict, OrderedDict
from base_caching import BaseCaching

class LFUCache(BaseCaching):
    def __init__(self):
        """Initialize the LFUCache with additional tracking structures."""
        super().__init__()
        self.frequency = defaultdict(int)  # Tracks the frequency of each key
        self.usage_order = OrderedDict()   # Tracks the order of key usage for ties in frequency

    def put(self, key, item):
        """Add an item to the cache, or update it if it already exists."""
        if key is None or item is None:
            return

        # If the cache already has the key, update its value and increase its frequency
        if key in self.cache_data:
            self.cache_data[key] = item
            self.frequency[key] += 1
            # Move the key to the end to mark it as recently used
            self.usage_order.move_to_end(key)
        else:
            # If cache is at capacity, remove the least frequently used item
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                # Find the least frequently used keys
                min_freq = min(self.frequency.values())
                # Find all keys with the least frequency
                least_used = [k for k, v in self.frequency.items() if v == min_freq]
                # Use LRU to pick the key to discard if there's a tie in frequency
                lru_key = next(k for k in self.usage_order.keys() if k in least_used)
                
                # Discard the selected key
                print(f"DISCARD: {lru_key}")
                self.cache_data.pop(lru_key)
                self.frequency.pop(lru_key)
                self.usage_order.pop(lru_key)

            # Insert the new key-value pair and initialize its frequency
            self.cache_data[key] = item
            self.frequency[key] = 1
            self.usage_order[key] = True  # Add to usage order to mark it as recently used

    def get(self, key):
        """Get an item from the cache and update its usage."""
        if key is None or key not in self.cache_data:
            return None

        # Update frequency and usage order of the key
        self.frequency[key] += 1
        self.usage_order.move_to_end(key)
        return self.cache_data[key]

    def print_cache(self):
        """Print the cache contents for debugging purposes."""
        print("Current cache:")
        for key, value in self.cache_data.items():
            print(f"{key}: {value}")
