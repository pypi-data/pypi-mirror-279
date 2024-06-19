"""
random_data_operations.py
=========
This module provides functions for generating random values.

Functions:
    - random_integer: Generates a random integer with `n` digits.
    - random_string: Generates a random string with `n` uppercase letters.
    - random_serial: Generates a random serial code with `n` alphanumeric characters.
"""

from string import digits, ascii_uppercase
from random import choice

def random_integer(n):
    """
    Generates a random integer with `n` digits.

    Args:
        n (int): The number of digits in the random integer.

    Returns:
        str: The randomly generated integer as a string.

    Example:
        >>> random_integer(3)
        '739'

    Raises:
        ValueError: If n is not a positive integer.
    """
    if not isinstance(n, int) or n <= 0:
        raise ValueError("n must be a positive integer")

    characters = digits
    password = ''.join(choice(characters) for i in range(n))
    return password

def random_string(n):
    """
    Generates a random string with `n` uppercase letters.

    Args:
        n (int): The length of the random string.

    Returns:
        str: The randomly generated string.

    Example:
        >>> random_string(5)
        'JVDHG'
    """
    characters = ascii_uppercase
    password = ''.join(choice(characters) for i in range(n))
    return str(password)

def random_serial(n):
    """
    Generates a random serial code with `n` alphanumeric characters.

    Args:
        n (int): The length of the random serial code.

    Returns:
        str: The randomly generated serial code.

    Example:
        >>> random_serial(8)
        '7X35B6F9'
    """
    characters = digits + ascii_uppercase
    password = ''.join(choice(characters) for i in range(n))
    return str(password)