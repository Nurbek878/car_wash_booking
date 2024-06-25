from datetime import date, datetime, time, timedelta


def round_to_next_hour(dt: datetime) -> datetime:
    '''
    Вспомогательная функция для округления даты до следующего часа.'''
    rounded = dt.replace(second=0, microsecond=0, minute=0, hour=dt.hour
                         ) + timedelta(hours=1)
    if 9 <= rounded.hour < 18:
        return rounded
    else:
        return (rounded + timedelta(days=1)).replace(hour=14)


FROM_TIME = round_to_next_hour(datetime.now()).isoformat(timespec='minutes')


async def get_working_hours(date_obj: date) -> tuple[datetime, datetime]:
    """
    Вспомогательная функция для получения начала и конца
    рабочего дня на указанную дату.
    """
    start_time = time(hour=9, minute=0)
    end_time = time(hour=18, minute=0)
    start_datetime = datetime.combine(date_obj, start_time)
    end_datetime = datetime.combine(date_obj, end_time)
    return start_datetime, end_datetime
