"""
color_operations.py
=========
This module provides functions for converting between hexadecimal and RGB color formats.

Functions:
    - hex_to_rgb: Convert a hexadecimal color code to RGB format.
    - rgb_to_hex: Convert an RGB color tuple to hexadecimal format.
"""

def hex_to_rgb(hex_code):
    """
    Convert a hexadecimal color code to RGB format.

    Args:
        hex_code (str): The hexadecimal color code (e.g., 'FFA500').

    Returns:
        tuple: A tuple representing the RGB values (e.g., (255, 165, 0)).

    Example:
        >>> hex_to_rgb('FFA500')
        (255, 165, 0)
    """
    hex_code = hex_code.lstrip('#')
    return tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    """
    Convert an RGB color tuple to hexadecimal format.

    Args:
        rgb (tuple): A tuple representing RGB values (e.g., (255, 165, 0)).

    Returns:
        str: The hexadecimal color code (e.g., 'FFA500').

    Example:
        >>> rgb_to_hex((255, 165, 0))
        '#ffa500'
    """
    return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])
