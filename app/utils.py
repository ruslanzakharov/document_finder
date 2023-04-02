from datetime import datetime as dt


def str_to_dt_obj(dt_str: str) -> dt:
    """Преобразует строку в datetime объект."""

    return dt.strptime(dt_str, '%Y-%m-%d %H:%M:%S')


def cur_datetime() -> dt:
    """Возвращает текущее время в правильном формате."""

    dt_now = dt.now()
    formatted_dt_now = dt(
        year=dt_now.year,
        month=dt_now.month,
        day=dt_now.day,
        hour=dt_now.hour,
        minute=dt_now.minute
    )

    return formatted_dt_now
