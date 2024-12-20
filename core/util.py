import sys

from core import logging
from core.updating import UpdateHandler


def get_or_none[T](lst: list[T], idx: int) -> (T | None):
    try:
        return lst[idx]
    except IndexError:
        return None

def terminate():
    UpdateHandler.instance.quit()
    UpdateHandler.instance.join()
    logging.force_flush()
    sys.exit(0)
