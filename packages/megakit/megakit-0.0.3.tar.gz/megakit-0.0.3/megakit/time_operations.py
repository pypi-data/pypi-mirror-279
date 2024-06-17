"""
time_operations.py
=======
This module provides functions for working with dates and time.

Variables:
    - months: A list of month names.

Functions:
    - get_date: Returns the current date in the format "MM/DD/YYYY".
    - get_month: Returns the current month index and name.
    - get_year: Returns the current year as an integer.
    - estimate_reading_time: Estimate reading time in minutes based on the number of words.
"""

from datetime import datetime, date

months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

def get_date():
    """
    Returns the current date in the format "MM/DD/YYYY".

    Returns:
        str: The current date in the format "MM/DD/YYYY".

    Example:
        >>> get_date()
        '07/02/2023'
    """
    today = date.today()
    d = today.strftime("%m/%d/%Y")
    return d

def get_month():
    """
    Returns the current month index and name.

    Returns:
        list: A list containing the current month index (0-11) and name.

    Example:
        >>> get_month()
        [6, 'July']
    """
    month_index = datetime.now().month - 1
    return [month_index, months[month_index]]

def get_year():
    """
    Returns the current year as an integer.

    Returns:
        int: The current year.

    Example:
        >>> get_year()
        2023
    """
    return int(datetime.now().year)

def estimate_reading_time(words_number):
    """
    Estimate reading time in minutes based on the number of words.

    Args:
        words_number (int): Number of words in the text.

    Returns:
        float: Estimated reading time in minutes.

    Raises:
        ValueError: If words_number is not a positive integer.
    """
    if not isinstance(words_number, int) or words_number <= 0:
        raise ValueError("words_number should be a positive integer")

    reading_time = (0.4615 / 60) * words_number
    return reading_time
