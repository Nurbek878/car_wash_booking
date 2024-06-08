from datetime import datetime, timedelta


def round_to_next_hour(dt: datetime) -> datetime:
    rounded = dt.replace(second=0, microsecond=0, minute=0, hour=dt.hour
                         ) + timedelta(hours=1)
    if 9 <= rounded.hour < 18:
        return rounded
    else:
        return (rounded + timedelta(days=1)).replace(hour=14)


FROM_TIME = round_to_next_hour(datetime.now()).isoformat(timespec='minutes')
