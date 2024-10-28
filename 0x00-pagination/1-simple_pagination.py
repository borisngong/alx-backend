#!/usr/bin/env python3
"""
A script to paginate through a dataset of popular baby names
"""
from typing import List, Tuple
import csv


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
    Calculate the start and end index for a specific page and page size
    """
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    return start_index, end_index


class Server:
    """Server class to paginate a database of popular baby names."""
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """
        Responsible for Loading the dataset from the CSV file if not
        already loaded
        """
        if self.__dataset is None:
            try:
                with open(self.DATA_FILE, newline='') as f:
                    reader = csv.reader(f)
                    dataset = [row for row in reader]
                self.__dataset = dataset[1:]
            except FileNotFoundError:
                print(f"Error: {self.DATA_FILE} not found.")
                self.__dataset = []

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """
        Retrieve a page of data from the dataset

        Args:
            page (int): The page number to retrieve
            page_size (int): The number of items per page

        Returns:
            List[List]: A list of records for the specified page
        """
        assert isinstance(page, int) and page > 0
        assert isinstance(page_size, int) and page_size > 0
        start_index, end_index = index_range(page, page_size)
        dataset = self.dataset()

        if start_index >= len(dataset):
            return []

        return dataset[start_index:end_index]
