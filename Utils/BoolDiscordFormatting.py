from datetime import datetime
import calendar


def evaluate_discord_timestamp(timestamp: int, timecheck: str) -> bool:

    def max_day_of_month(curr_year: int, curr_month: int) -> int:
        _, num_days = calendar.monthrange(curr_year, curr_month)
        return num_days

    message_time = datetime.fromtimestamp(timestamp)

    if timecheck.startswith("during:"):
        date_part = timecheck[len("during:"):]
        if "-" in date_part:
            date_components = date_part.split("-")
            if len(date_components) == 2:
                year, month = map(int, date_components)
                return message_time.year == year and message_time.month == month
            elif len(date_components) == 3:
                year, month, day = map(int, date_components)
                return (
                        message_time.year == year
                        and message_time.month == month
                        and message_time.day == day
                )
        else:
            year = int(date_part)
            return message_time.year == year

    elif timecheck.startswith("after:"):
        date_part = timecheck[len("after:"):]
        date_components = date_part.split("-")
        if len(date_components) == 1:
            year = int(date_components[0])
            check_time = datetime(year, 12, 31)
        elif len(date_components) == 2:
            year, month = map(int, date_components)
            check_time = datetime(year, month, max_day_of_month(year, month))
        else:
            year, month, day = map(int, date_components)
            check_time = datetime(year, month, day)
        return message_time > check_time

    elif timecheck.startswith("before:"):
        date_part = timecheck[len("before:"):]
        date_components = date_part.split("-")
        if len(date_components) == 1:
            year = int(date_components[0])
            check_time = datetime(year, 1, 1)
        elif len(date_components) == 2:
            year, month = map(int, date_components)
            check_time = datetime(year, month, 1)
        else:
            year, month, day = map(int, date_components)
            check_time = datetime(year, month, day)
        return message_time < check_time

    raise ValueError("Invalid timecheck format.")
