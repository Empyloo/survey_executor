import datetime as dt
from typing import Union


# Update the calculate_next_run_time function to use mocked_today as the current date
def calculate_next_run_time(
    frequency: str, time_of_day: str, today: Union[dt.datetime, None] = None
) -> dt.datetime:
    if today is None:
        today = dt.datetime.now()

    freq_to_days = {
        "daily": 1,
        "weekly": 7,
        "fortnightly": 14,
        "monthly": 30,
        "quarterly": 91,
        "annually": 365,
    }

    time = dt.datetime.strptime(time_of_day, "%H:%M").time()
    days = freq_to_days[frequency]

    next_run_date = today + dt.timedelta(days=days)

    if next_run_date.weekday() >= 5:  # 5, 6 corresponds to Saturday, Sunday
        next_run_date = next_run_date + dt.timedelta(days=7 - next_run_date.weekday())

    return dt.datetime.combine(next_run_date.date(), time)


if __name__ == "__main__":
    # Mock current date to be a Friday
    mocked_today = dt.datetime(2023, 7, 28, 10, 0, 0)
    # Test the function with the mocked today's date
    for freq in ["daily", "weekly", "fortnightly", "monthly", "quarterly", "annually"]:
        print(
            f"For {freq} frequency at 10:00, the next run time will be: {calculate_next_run_time(freq, '10:00', mocked_today)}"
        )
