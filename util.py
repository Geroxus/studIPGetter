"""diverse helper functions"""


def string_between(string: str, before: str, after: str) -> str:
    """helper function to get a string between two other substrings
    :param string:
    :param before:
    :param after:
    :return:
    """
    return string.split(before)[1].split(after)[0]
