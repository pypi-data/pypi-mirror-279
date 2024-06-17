"""
string_operations.py
=========
This module provides functions for manipulating strings.

Functions:
    - get_first_characters: Get the first `chars` characters of a string.
    - get_last_characters: Get the last `chars` characters of a string.
    - reverse_string: Reverse a given string.
    - number_of_words: Count the number of words in a string.
"""

def get_first_characters(s, chars):
    """
    Get the first `chars` characters of a string.

    Args:
        s (str): The input string.
        chars (int): Number of characters to retrieve from the start.

    Returns:
        str: The first `chars` characters of the string `s`.

    Example:
        >>> get_first_characters("Hello, world!", 5)
        'Hello'
    """
    return s[:chars]

def get_last_characters(s, chars):
    """
    Get the last `chars` characters of a string.

    Args:
        s (str): The input string.
        chars (int): Number of characters to retrieve from the end.

    Returns:
        str: The last `chars` characters of the string `s`.

    Example:
        >>> get_last_characters("Hello, world!", 6)
        'world!'
    """
    return s[-chars:]

def reverse_string(s):
    """
    Reverse a given string.

    Args:
        s (str): The input string.

    Returns:
        str: The reversed string.

    Example:
        >>> reverse_string("hello")
        'olleh'
    """
    return s[::-1]

def number_of_words(title):
    """
    Count the number of words in a string.

    Args:
        title (str): The input string.

    Returns:
        int: Number of words in the string.

    Example:
        >>> number_of_words("Hello, world!")
        2
    """
    return len(title.split())
