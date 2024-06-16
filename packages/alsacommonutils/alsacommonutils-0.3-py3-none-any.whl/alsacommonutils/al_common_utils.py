from datetime import date, datetime, timedelta, timezone

def get_datetime_ranges(diff_hours,fmt="%Y-%m-%dT%H:%M:%SZ"):
    current_time = datetime.now(timezone.utc)
    previous_time = current_time - timedelta(hours=diff_hours)
    return previous_time.strftime(fmt), current_time.strftime(fmt)

def string_to_list(value,separator):
    return [key.strip() for key in value.split(separator) if key.strip()]