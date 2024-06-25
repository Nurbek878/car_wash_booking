from datetime import date, time


async def get_working_hours(date_obj: date) -> list:
    """
    Вспомогательная функция для получения общего рабочего времени.
    """
    start_time = time(hour=9, minute=0)
    end_time = time(hour=18, minute=0)
    return list(range(start_time.hour, end_time.hour))
