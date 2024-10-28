#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""

import csv
from typing import List, Dict, Optional


class Server:
    """Server class to paginate a database of popular baby names."""
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List[str]]:
        """Load and cache the dataset, excluding the header row."""
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]  # Skip the header row
        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List[str]]:
        """Create an indexed dataset for deletion-resilient pagination.

        Returns:
            Dict[int, List[str]]: Dataset indexed by position.
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {
                i: truncated_dataset[i] for i in range(len(truncated_dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None,
                        page_size: int = 10) -> Dict:
        """Return pagination data and metadata."""
        # Validate the provided index
        assert index is not None and 0 <= index < len(self.indexed_dataset())

        data = []
        current_index = index
        count = 0
        indexed_data = self.indexed_dataset()

        # Gather items for the current page, handling any deletions
        while count < page_size and current_index < len(indexed_data):
            item = indexed_data.get(current_index)
            if item is not None:
                data.append(item)
                count += 1
            current_index += 1

        next_index = (current_index if current_index < len(indexed_data)
                      else None)

        return {
            "index": index,
            "next_index": next_index,
            "page_size": len(data),
            "data": data
        }
