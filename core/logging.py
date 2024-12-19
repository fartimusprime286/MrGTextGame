import threading
import datetime

log_file = "DEBUG.log"
buffer_line_limit = 100
_buffer = []

with open(log_file, "w") as log:
    log.write("")

def debug(msg):
    date = datetime.datetime.now()
    date_formatted = date.strftime("%y-%m-%d %H:%M:%S")

    _buffer.append(f"[{threading.current_thread().name}] ({date_formatted}): {msg}\n")

def attempt_flush():
    if len(_buffer) >= buffer_line_limit:
        force_flush()

def force_flush():
    with open(log_file, "a") as log:
        log.writelines(_buffer)

    _buffer.clear()