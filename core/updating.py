import time
import logging
from threading import Thread, Event
from typing import Self

from core.game import SceneKonsoleBuffer
from core.timestack import TimeStack


class UpdateHandler:
    instance: (Self | None) = None

    def __init__(self, buffer: SceneKonsoleBuffer):
        if UpdateHandler.instance is not None:
            raise Exception("This class is a singleton!")

        UpdateHandler.instance = self

        self._buffer = buffer
        self._tick_rate = 20
        self._time_stack = TimeStack()
        self._thread: (Thread | None) = None-0
        self._stop_running = Event()

    def set_tick_rate(self, tick_rate):
        self._tick_rate = tick_rate

    def launch(self):
        if self._thread is None:
            self._thread = Thread(target=self._update_loop, name="UpdateHandler")

        self._thread.start()

    def quit(self):
        self._stop_running.set()

    def join(self):
        self._thread.join()

    def _update_loop(self):
        try:
            while not (self._buffer.should_quit() or self._stop_running.is_set()):
                tick_rate_target_ms = 1000 / self._tick_rate
                start_time = time.perf_counter_ns()

                self._buffer.update()

                end_time = time.perf_counter_ns()
                elapsed_time_ms = (end_time - start_time) / 1000000
                sleep_time_ms = tick_rate_target_ms - elapsed_time_ms
                if sleep_time_ms > 0:
                    time.sleep(sleep_time_ms / 1000)
        except Exception as ex:
            logging.error("Error while updating scene", exc_info=ex)
            logging.error("Terminating...")
            self._buffer.quit()
            self._stop_running.set()
