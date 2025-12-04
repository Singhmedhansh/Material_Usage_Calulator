"""
utils.py — input validation helpers to make the app robust against bad user input.
"""

from typing import Tuple


def get_positive_float(prompt: str) -> float:
    """
    Prompt the user until they enter a valid positive float (>= 0).
    Returns the float value.
    """
    while True:
        s = input(prompt).strip()
        try:
            v = float(s)
            if v < 0:
                print("Please enter a non-negative number.")
                continue
            return v
        except ValueError:
            print("Invalid number. Please try again.")


def get_positive_int(prompt: str, default: int = None) -> int:
    """
    Prompt until a valid non-negative integer is entered.
    If default is provided and user enters empty string, returns default.
    """
    while True:
        s = input(prompt).strip()
        if s == "" and default is not None:
            return default
        try:
            v = int(s)
            if v < 0:
                print("Please enter a non-negative integer.")
                continue
            return v
        except ValueError:
            print("Invalid integer. Please try again.")


def yes_no(prompt: str) -> bool:
    """
    Ask a yes/no question. Returns True for yes, False for no.
    """
    while True:
        s = input(f"{prompt} (y/n): ").strip().lower()
        if s in ("y", "yes"):
            return True
        if s in ("n", "no"):
            return False
        print("Please answer 'y' or 'n'.")


def parse_tile_size(tile_str: str) -> Tuple[float, float]:
    """
    Parse tile size like '2x2' or '0.6x0.6' into (length, width) floats.
    Raises ValueError on bad format.
    """
    s = tile_str.strip().lower().replace(" ", "")
    parts = s.split("x")
    if len(parts) != 2:
        raise ValueError("Tile size must be like '2x2' or '0.6x0.6'")
    try:
        l = float(parts[0])
        w = float(parts[1])
    except ValueError:
        raise ValueError("Tile dimensions must be numbers.")
    if l <= 0 or w <= 0:
        raise ValueError("Tile dimensions must be positive.")
    return l, w
