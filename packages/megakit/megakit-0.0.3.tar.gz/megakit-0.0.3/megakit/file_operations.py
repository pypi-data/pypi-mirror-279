"""
file_operations.py
=========
This module provides functions for managing files and directories in Python.

Functions:
- read_lines(file_path): Read all lines from a text file.
- count_lines(file_path): Count the number of lines in a text file.
- count_folders(folder_path): Count the number of subdirectories in a folder.
- count_files(folder_path): Count the number of files in a folder.
- get_file_info(file_path): Get information about a file (name, extension, location).
- get_file_name(file_path): Get the name of a file.
- get_file_extension(file_path): Get the extension of a file.
- get_file_location(file_path): Get the directory containing a file.
- is_file(path): Check if a path points to a file.
- is_folder(path): Check if a path points to a directory.
- is_existing(path): Check if a path exists.
- list_directories(folder_path): List directories in a folder.
- list_files(folder_path): List files in a folder.
- is_empty(folder_path): Check if a folder is empty.
- delete_file(file_path): Delete a file.
- delete_folder(folder_path): Delete a folder and all its contents recursively.

Note:
- Error handling should be implemented where applicable to handle potential exceptions.
- Ensure paths provided to these functions are valid and accessible.
"""

import os
import shutil

def read_lines(file_path):
    """
    Read all lines from a text file.

    Args:
        file_path (str): Path to the file.

    Returns:
        list: A list of strings, each string representing a line from the file.
    """
    with open(file_path) as f:
        lines = f.readlines()
    return lines

def count_lines(file_path):
    """
    Count the number of lines in a text file.

    Args:
        file_path (str): Path to the file.

    Returns:
        int: Number of lines in the file.
    """
    return len(read_lines(file_path))

def count_folders(folder_path):
    """
    Count the number of subdirectories in a folder.

    Args:
        folder_path (str): Path to the folder.

    Returns:
        int: Number of subdirectories in the folder.
    """
    return len(list_directories(folder_path))

def count_files(folder_path):
    """
    Count the number of files in a folder.

    Args:
        folder_path (str): Path to the folder.

    Returns:
        int: Number of files in the folder.
    """
    return len(list_files(folder_path))


def get_file_info(file_path):
    """
    Get information about a file.

    Args:
        file_path (str): Path to the file.

    Returns:
        tuple: (file_name, file_extension, file_location)
    """
    file_name = os.path.basename(file_path)
    file_extension = os.path.splitext(file_path)[1]
    file_location = os.path.dirname(file_path)
    return file_name, file_extension, file_location

def get_file_name(file_path):
    """
    Get the name of a file.

    Args:
        file_path (str): Path to the file.

    Returns:
        str: Name of the file.
    """
    return os.path.basename(file_path)

def get_file_extension(file_path):
    """
    Get the extension of a file.

    Args:
        file_path (str): Path to the file.

    Returns:
        str: Extension of the file.
    """
    return os.path.splitext(file_path)[1]

def get_file_location(file_path):
    """
    Get the directory containing a file.

    Args:
        file_path (str): Path to the file.

    Returns:
        str: Directory containing the file.
    """
    return os.path.dirname(file_path)

def is_file(path):
    """
    Check if a path points to a file.

    Args:
        path (str): Path to check.

    Returns:
        bool: True if the path points to a file, False otherwise.
    """
    return os.path.isfile(path)

def is_folder(path):
    """
    Check if a path points to a directory.

    Args:
        path (str): Path to check.

    Returns:
        bool: True if the path points to a directory, False otherwise.
    """
    return os.path.isdir(path)

def is_existing(path):
    """
    Check if a path exists.

    Args:
        path (str): Path to check.

    Returns:
        bool: True if the path exists, False otherwise.
    """
    return os.path.exists(path)

def list_directories(folder_path):
    """
    List directories in a folder.

    Args:
        folder_path (str): Path to the folder.

    Returns:
        list: List of directory names.
    """
    return [os.path.join(folder_path, name) for name in os.listdir(folder_path)
            if os.path.isdir(os.path.join(folder_path, name))]

def list_files(folder_path):
    """
    List files in a folder.

    Args:
        folder_path (str): Path to the folder.

    Returns:
        list: List of file names.
    """
    return [name for name in os.listdir(folder_path)
            if os.path.isfile(os.path.join(folder_path, name)) and not name.startswith(".")]

def is_empty(folder_path):
    """
    Check if a folder is empty.

    Args:
        folder_path (str): Path to the folder.

    Returns:
        bool: True if the folder is empty, False otherwise.
    """
    return not os.listdir(folder_path)

def delete_file(file_path):
    """
    Delete a file.

    Args:
        file_path (str): Path to the file to delete.
    """
    os.remove(file_path)

def delete_folder(folder_path):
    """
    Delete a folder and all its contents recursively.

    Args:
        folder_path (str): Path to the folder to delete.
    """
    shutil.rmtree(folder_path)