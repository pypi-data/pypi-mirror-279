import re

from unidecode import unidecode


def cannonize(input_str):
    """
    Remove non-alphanumeric characters from the input string, convert it to lowercase, and replace accented characters with their non-accented equivalents.

    Args:
        input_str (str): The input string to be cannonized.

    Returns:
        str: The cannonized string with non-alphanumeric characters removed, converted to lowercase, and accented characters replaced with their non-accented equivalents.
    """
    if input_str:
        # Remove non-alphanumeric characters and convert to lowercase
        cannonized_str = re.sub(r"\W", "", input_str.lower(), flags=re.UNICODE)
        # Replace accented characters with their non-accented equivalents
        cannonized_str = unidecode(cannonized_str)
        return cannonized_str
    return ""
