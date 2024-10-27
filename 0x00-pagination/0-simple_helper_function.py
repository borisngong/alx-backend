#!/usr/bin/env python3
"""
Module for working with pagination returning a tuple of start and end index
"""
from typing import Tuple


def index_range(page: int, page_size: int) -> Tuple:
    """
    Responsible for returning a tuple containing a start index and an end
    index for pagination
    """
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    return (start_index, end_index)
