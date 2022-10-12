"""Utils package

Defines utility functions : generate_key
"""
import random
import string


def generate_key(size: int = 5) -> str:
    """Generate key

    Creates a random key of length `size` composed of :
    - lowercase characters [a-z]
    - uppercase characters [A-Z]
    - digits [0-9]

    Number of possible unique keys of size N = (26*2+10)^N
    - size = 1 => 62 unique keys
    - size = 2 => 3844 unique keys
    - size = 3 => 238328 unique keys
    - size = 5 => ~916e6 unique keys
    - size = 8 => ~218e12 unique keys
    - size = 13 => ~2e23 unique keys
    - ...

    Args:
        size (int, optional): size of the random key string. Defaults to 5.

    Returns:
        str: random key string of size `size`
    """
    return "".join(
        random.choices(string.ascii_uppercase + string.digits, k=size)  # nosec B311
    )
