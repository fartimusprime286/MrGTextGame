import sys

from core import logging
from core.game import SceneKonsoleBuffer
from core.updating import UpdateHandler

buffer: SceneKonsoleBuffer

ending: str

def get_or_none[T](lst: list[T], idx: int) -> (T | None):
    try:
        return lst[idx]
    except IndexError:
        return None

def terminate(ending_msg: str):
    global ending

    UpdateHandler.instance.quit()
    UpdateHandler.instance.join()
    buffer.quit()
    logging.force_flush()
    ending = ending_msg
    sys.exit(0)
