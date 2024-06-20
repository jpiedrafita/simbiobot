from datetime import datetime


def check_time_format(time_str):
    """
    Checks if the given time string matches the accepted format: 'HH:MM'
    """
    try:
        datetime.strptime(time_str, "%H:%M")
        return True
    except ValueError:
        return False


def check_date_format(date_str):
    """
    Checks if the given date string matches any of the accepted formats:
    'dd-mm-yyyy', 'dd/mm/yyyy', 'yyyy-mm-dd'
    """
    formats = ["%d-%m-%Y", "%d/%m/%Y", "%Y-%m-%d"]
    for fmt in formats:
        try:
            datetime.strptime(date_str, fmt)
            return True
        except ValueError:
            continue
    return False
