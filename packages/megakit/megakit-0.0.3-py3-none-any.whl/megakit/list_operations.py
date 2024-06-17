"""
list_operations.py
=========
This module provides functions for working with lists.

Functions:
    - has_duplicates: Check if a list has duplicate elements.
    - print_options: Print options from a list with each option indexed.
"""

def has_duplicates(lst):
    """
    Check if a list has duplicate elements.

    Args:
        lst (list): The list to check for duplicates.

    Returns:
        bool: True if the list has duplicates, False otherwise.

    Example:
        >>> has_duplicates([1, 2, 3, 3, 4])
        True
        >>> has_duplicates([1, 2, 3, 4])
        False
    """
    return len(lst) != len(set(lst))

def print_options(lst):
    """
    Print options from a list with each option indexed.

    Args:
        list (list): The list of options to print.

    Example:
        >>> print_options(['Option A', 'Option B', 'Option C'])
        1. Option A
        2. Option B
        3. Option C
    """
    for index, option in enumerate(lst):
        print(f"{index+1}. {option}")
