from datetime import datetime, timedelta


def isfloat(num):
    """validate the value is float or

    Args:
        num (Any): number

    Returns:
        bool: is float or not
    """
    try:
        float(num)
        return True
    except ValueError:
        return False


def is_valid_search_criteria(search_criteria, search_by_department=False):
    """function that accept dict object to validated every value of this object

    Args:
        search_criteria (dict): object contain as keys radius_km, start_date, end_date, longitude, latitude, address

    Returns:
        bool: valide or not valide
    """
    try:
        allowed_raduis = [0.99, 5, 10, 15, 20, 25, 30]
        if search_by_department:
            allowed_raduis.append(100)

        valide = (
            float(search_criteria["radius_km"]) in allowed_raduis
            and bool(datetime.strptime(search_criteria["start_date"], "%Y-%m-%d"))
            and bool(datetime.strptime(search_criteria["end_date"], "%Y-%m-%d"))
            and isfloat(float(search_criteria["longitude"]))
            and isfloat(float(search_criteria["latitude"]))
        )
    except ValueError:
        valide = False
    return valide


def capitalize_custom(name: str) -> str:
    """Capitalize the first letter of every word with some exceptions

    Args:
        name : str

    Returns:
        name : str
    """
    result = name.title()
    lower_words = ["Sur", "La", "Le", "Les", "Lès", "De", "Des", "En", "Et", "Aux"]
    for lower_word in lower_words:
        result = (
            result.replace("-" + lower_word + "-", "-" + lower_word.lower() + "-")
            .replace(" " + lower_word + "-", " " + lower_word.lower() + "-")
            .replace(" " + lower_word + " ", " " + lower_word.lower() + " ")
        )

    result = (
        result.replace(" L'", " l'")
        .replace(" D'", " d'")
        .replace("-L'", "-l'")
        .replace("-D'", "-d'")
    )

    return result


def is_date_after_paris_datetime(date: datetime) -> bool:
    """Check if the date is after the current date in Paris timezone

    Args:
        date : datetime

    Returns:
        bool
    """
    utc_time = datetime.utcnow()
    paris_offset = timedelta(hours=1)
    paris_time = utc_time + paris_offset
    return date < paris_time
