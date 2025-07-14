from datetime import timedelta, datetime

DATE_FORMATS = {
    "default": "%Y-%m-%d",
    "iso": "%Y-%m-%dT%H:%M:%SZ",
    "compact": "%Y%m%d",
    "datetime": "%Y-%m-%d %H:%M:%S"
}

def generate_date_ranges(start_date, end_date, date_format="default", granularity="daily"):
    if date_format not in DATE_FORMATS:
        raise ValueError(f"Invalid date_format '{date_format}'. Supported: {list(DATE_FORMATS.keys())}")

    date_format_str = DATE_FORMATS[date_format]
    print(f"Using date format: {date_format_str}")
    print(f"Generating date range from {start_date} to {end_date} with granularity '{granularity}'")
    
    start_dt = parse_date(start_date, date_format_str)
    end_dt = parse_date(end_date, date_format_str)

    report_dates = []
    current_dt = start_dt
    if granularity == "hourly":
        delta = timedelta(hours=1)
    else:  # default to daily
        delta = timedelta(days=1)

    while current_dt <= end_dt:
        report_dates.append(current_dt)
        current_dt += delta

    return report_dates


def parse_date(value, date_format_str):
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        try:
            return datetime.strptime(value, date_format_str)
        except ValueError as e:
            raise ValueError(f"Cannot parse '{value}' with format '{date_format_str}': {e}")
    raise ValueError(f"Unsupported date type: {type(value)}")
