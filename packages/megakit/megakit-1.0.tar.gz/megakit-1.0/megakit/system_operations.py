"""
system_operations.py
=========
This module provides functions for interacting with subprocesses and platform-specific operations.

Functions:
    - clear_terminal: Clear the terminal screen.
    - close_finder_windows: Close all Finder windows on macOS using AppleScript.
"""

import subprocess
import platform

def clear_terminal():
    """
    Clear the terminal screen.

    Uses 'cls' for Windows and '\033c' for other platforms.

    Example:
        >>> clear_terminal()
    """
    if platform.system() == "Windows":
        subprocess.Popen("cls", shell=True).communicate()
    else:
        print("\033c", end="")

def close_finder_windows():
    """
    Close all Finder windows on macOS using AppleScript.

    Example:
        >>> close_finder_windows()
    """
    if platform.system() == "Darwin":
        applescript = """
        tell application "Finder"
            close every window
        end tell
        """
        subprocess.call(['osascript', '-e', applescript])
    else:
        print("Functionality not supported on this platform.")
