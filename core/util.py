import sys

from core import logging
from core.updating import UpdateHandler


def get_or_none[T](lst: list[T], idx: int) -> (T | None):
    try:
        return lst[idx]
    except IndexError:
        return None

def terminate(ending_msg: str):
    UpdateHandler.instance.quit()
    UpdateHandler.instance.join()
    logging.force_flush()
    print(ending_msg)
    sys.exit(0)
