def snake_to_camel_case(snake_str: str) -> str:
    """Converts a snake_case string to camelCase.

    Args:
        snake_str (str): A snake_case string.

    Returns:
        str: A camelCase string.
    """
    if "_" in snake_str:
        text = "".join(x.capitalize() or "_" for x in snake_str.split("_"))
        return text[0].lower() + text[1:]
    else:
        return snake_str


def snake_to_pascal_case(snake_str: str) -> str:
    """Converts a snake_case string to PascalCase.

    Args:
        snake_str (str): A snake_case string.

    Returns:
        str: A PascalCase string.
    """
    if "_" in snake_str:
        return "".join(x.capitalize() for x in snake_str.split("_"))
    else:
        return snake_str.capitalize()
