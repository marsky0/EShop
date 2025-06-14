import datetime

def current_timestamp() -> int:
    return int(datetime.datetime.now(datetime.UTC).timestamp())

def current_datetime() -> int:
    return int(datetime.datetime.now(datetime.UTC).timestamp())
