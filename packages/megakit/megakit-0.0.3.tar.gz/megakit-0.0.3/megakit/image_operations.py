"""
image_operations.py
=========
This module provides functions for working with images.

Functions:
    - add_padding: Adds padding to an image.
    - round_corners: Rounds the corners of an image.
    - turn_to_square: Converts an image into a square by adding background color.
"""

from PIL import Image
from aggdraw import Draw, Brush

def add_padding(image_path, padding_value, color):
    """
    Adds padding to an image.

    Args:
        image_path (str): The path to the image file.
        padding_value (int): The amount of padding in pixels to be added on all sides of the image.
        color (tuple): The RGB color tuple (red, green, blue) or RGBA color tuple (red, green, blue, alpha)
            to fill the padding area with.

    Returns:
        None: This function does not return any value. The modified image is saved with the same name
        at the specified `image_path`.

    Raises:
        FileNotFoundError: If the specified `image_path` does not exist.
    """
    image = Image.open(image_path)
    top = right = bottom = left = padding_value
    width, height = image.size
    new_width = width + right + left
    new_height = height + top + bottom
    result = Image.new(image.mode, (new_width, new_height), color)
    result.paste(image, (left, top))
    result.save(image_path)


def round_corners(image_path, radius):
    """
    Rounds the corners of an image.

    Args:
        image_path (str): The path to the image file.
        radius (int): The radius of the rounded corners in pixels.

    Returns:
        None: This function does not return any value. The modified image is saved with the same name
        at the specified `image_path`.

    Raises:
        FileNotFoundError: If the specified `image_path` does not exist.
    """
    image = Image.open(image_path)
    mask = Image.new('L', image.size)
    draw = Draw(mask)
    brush = Brush('white')
    width, height = mask.size
    draw.pieslice((0, 0, radius*2, radius*2), 90, 180, 255, brush)
    draw.pieslice((width - radius*2, 0, width, radius*2), 0, 90, None, brush)
    draw.pieslice((0, height - radius * 2, radius *
                   2, height), 180, 270, None, brush)
    draw.pieslice((width - radius * 2, height - radius *
                   2, width, height), 270, 360, None, brush)
    draw.rectangle((radius, radius, width - radius, height - radius), brush)
    draw.rectangle((radius, 0, width - radius, radius), brush)
    draw.rectangle((0, radius, radius, height-radius), brush)
    draw.rectangle((radius, height-radius, width-radius, height), brush)
    draw.rectangle((width-radius, radius, width, height-radius), brush)
    draw.flush()
    image = image.convert('RGBA')
    image.putalpha(mask)
    image.save(image_path)


def turn_to_square(image_path, color):
    """
    Converts an image into a square by adding background color.

    Args:
        image_path (str): The path to the image file.
        color (tuple): The RGB color tuple (red, green, blue) or RGBA color tuple (red, green, blue, alpha)
            to fill the background of the square image with.

    Returns:
        None: This function does not return any value. The modified image is saved with the same name
        at the specified `image_path`.

    Raises:
        FileNotFoundError: If the specified `image_path` does not exist.
    """
    image = Image.open(image_path)
    x, y = image.size
    size = max(256, x, y)
    new_image = Image.new('RGB', (size, size), color = color)
    new_image.paste(image, (int((size - x) / 2), int((size - y) / 2)))
    new_image.save(image_path)