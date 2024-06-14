"""Demo of https://github.com/sgraaf/cookiecutter-python-package."""

__version__ = "0.1.0"


def add_one(x: int) -> int:
    """Add one to the input.

    Example:
        >>> from cookiecutter_python_package_demo import add_one
        >>> add_one(1)
        2

    Args:
        x: The input.

    Returns:
        The input plus one.
    """
    return x + 1
