import random


def random_amount() -> float:
    """Generate a random amount between 0.01 and 1000

    Returns:
        float: Random float with two decimal places
    """
    # ensure that there are two decimal places
    return round(random.uniform(0.01, 1000), 2)


def random_double_precision_array() -> str:
    """Generate a random double precision array

    Returns:
        str: Random double precision array as a string
    """
    return "{" + f"{round(random.uniform(0.01, 1000), 2)}" + "}"
