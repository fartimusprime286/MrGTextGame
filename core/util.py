def get_or_none[T](lst: list[T], idx: int) -> (T | None):
    try:
        return lst[idx]
    except IndexError:
        return None