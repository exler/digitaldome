def format_time_spent(time_spent: int) -> str:
    """
    Formats time spent in minutes to a human readable format.
    """
    hours, minutes = divmod(time_spent, 60)
    if hours and minutes:
        return f"{hours}h {minutes}m"
    elif hours:
        return f"{hours}h"
    else:
        return f"{minutes}m"


def make_imdb_url(imdb_id: str) -> str:
    return f"https://www.imdb.com/title/{imdb_id}/"
