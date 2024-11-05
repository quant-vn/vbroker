from datetime import datetime, timedelta


def split_date_range(start_date, end_date, days_interval=7):
    """
    Splits a date range into smaller intervals of a specified number of days.
    Args:
        start_date (str): The start date of the range in 'YYYY-MM-DD' format.
        end_date (str): The end date of the range in 'YYYY-MM-DD' format.
        days_interval (int, optional): The number of days for each interval. Defaults to 7.
    Returns:
        list of tuple: A list of tuples where each tuple contains the start and end date of an
        interval in 'YYYY-MM-DD' format.
    """
    current = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')

    intervals = []

    while current < end:
        interval_end = min(current + timedelta(days=days_interval-1), end)
        intervals.append((
            current.strftime('%Y-%m-%d'),
            interval_end.strftime('%Y-%m-%d')
        ))
        current = interval_end + timedelta(days=1)
    return intervals
