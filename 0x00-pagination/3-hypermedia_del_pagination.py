#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""

import csv
import math
from typing import List, Dict


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
        """
        Responsible for returning pagination data and metadata
        """
        # Validate the provided index
        assert index is not None and 0 <= index < len(self.indexed_dataset())

        data = []
        cur_idx = index
        count = 0

        # Loop to gather items for the current page, adapting to any deletions
        while count < page_size and cur_idx < len(self.indexed_dataset()):
            item = self.indexed_dataset().get(cur_idx)
            if item is not None:
                data.append(item)
                count += 1
            cur_idx += 1

        next_index = cur_idx if cur_idx < len(self.indexed_dataset()) else None

        return {
            "index": index,
            "next_index": next_index,
            "page_size": len(data),
            "data": data
        }
