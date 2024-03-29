# Path: src/utils/campaign_duration.py
"""
This module contains the functions to calculate the duration of a campaign.

"""
from datetime import datetime, timedelta
from typing import Optional


from datetime import datetime

def parse_time_of_day(time_str: str) -> (int, int):
    try:
        # Parse the time using Python's datetime, assuming the time is in 12-hour format with AM/PM
        parsed_time = datetime.strptime(time_str, "%I:%M %p")
    except ValueError:
        # Handle the case where the time is in 24-hour format
        parsed_time = datetime.strptime(time_str, "%H:%M")

    return parsed_time.hour, parsed_time.minute

def calculate_duration_time(
    type: str, duration: str, time_of_day: Optional[str] = None
) -> datetime:
    now = datetime.now()

    # Extract the duration unit and value
    duration_unit = duration[-1]  # Last character (m, h, d, w, M)
    duration_value = int(duration[:-1])  # All but the last character

    if type == "instant":
        if duration_unit == "m":
            return now + timedelta(minutes=duration_value)
        elif duration_unit == "h":
            return now + timedelta(hours=duration_value)
        elif duration_unit == "d":
            return now + timedelta(days=duration_value)
        elif duration_unit == "w":
            return now + timedelta(weeks=duration_value)
        else:
            raise ValueError("Invalid duration format")
    elif type == "recurring":
        if not time_of_day:
            raise ValueError("time_of_day is required for recurring type")

        hours, minutes = parse_time_of_day(time_of_day)

        if duration_unit == "d":
            return datetime(now.year, now.month, now.day, hours, minutes) + timedelta(
                days=duration_value
            )
        elif duration_unit == "w":
            return datetime(now.year, now.month, now.day, hours, minutes) + timedelta(
                weeks=duration_value
            )
        else:
            raise ValueError("Invalid duration format for recurring type")
    else:
        raise ValueError("Invalid type")


def is_over_29_days(date: datetime) -> bool:
    """Check if a date is more than 29 days away."""
    return (date.date() - datetime.now().date()).days > 29


if __name__ == "__main__":

    # Test the function
    print(parse_time_of_day("7:55 AM"))  # Output should be (7, 55)
    print(parse_time_of_day("7:55 PM"))  # Output should be (19, 55)
    print(parse_time_of_day("19:55"))    # Output should be (19, 55)

    # Test the function
    print(calculate_duration_time("instant", "5m"))
    print(calculate_duration_time("instant", "5h"))
    print(calculate_duration_time("recurring", "2w", "09:00"))

    # Test the is_over_29_days function
    print(is_over_29_days(datetime.now() + timedelta(days=30)))  # Expected: True
    print(is_over_29_days(datetime.now() + timedelta(days=29)))  # Expected: False
    print(is_over_29_days(datetime.now() + timedelta(days=28)))  # Expected: False

    
