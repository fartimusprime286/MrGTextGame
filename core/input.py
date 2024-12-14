import threading
from typing import Callable, Self

import keyboard

from core.game import SceneKonsoleBuffer


class Keybinding:
    def __init__(self, key: str):
        self.key = key
        self.press_callbacks = []
        self.release_callbacks = []
        self._lock = threading.Lock()

    def on_press(self, callback: Callable[[SceneKonsoleBuffer], None]):
        with self._lock:
            self.press_callbacks.append(callback)

    def on_release(self, callback: Callable[[SceneKonsoleBuffer], None]):
        with self._lock:
            self.release_callbacks.append(callback)

    def remove_on_press(self, callback: Callable[[SceneKonsoleBuffer], None]):
        with self._lock:
            self.press_callbacks.remove(callback)

    def remove_on_release(self, callback: Callable[[SceneKonsoleBuffer], None]):
        with self._lock:
            self.release_callbacks.remove(callback)

    def invoke_press(self, buffer: SceneKonsoleBuffer):
        with self._lock:
            for callback in self.press_callbacks:
                callback(buffer)

    def invoke_release(self, buffer: SceneKonsoleBuffer):
        with self._lock:
            for callback in self.release_callbacks:
                callback(buffer)


class InputHandler:
    instance: (Self | None) = None

    def __init__(self, buffer: SceneKonsoleBuffer):
        self.buffer = buffer
        self._bindings: dict[str, dict[str, Keybinding]] = dict()
        self._zone_queue: list[str] = list()
        self._bind_queue: list[(str, str)] = list()
        keyboard.on_press(self._on_press_key)
        keyboard.on_release(self._on_release_key)
        InputHandler.instance = self

    @staticmethod
    def create(buffer: SceneKonsoleBuffer):
        if InputHandler.instance is not None:
            return InputHandler.instance
        else: return InputHandler(buffer)

    def unbind_zone(self, zone: str):
        self._zone_queue.append(zone)

    def unbind(self, key: str, zone: str = "default_zone"):
        self._bind_queue.append((zone, key))

    def process_unbinds(self):
        for zone in self._zone_queue:
            self._bindings.pop(zone, None)
        for zone, key in self._bind_queue:
            zone_binds = self._bindings.get(zone, {})
            zone_binds.pop(key, None)

        self._zone_queue.clear()
        self._bind_queue.clear()

    def get_or_create_keybind(self, key: str, zone: str = "default_zone") -> Keybinding:
        bindings = self._bindings.get(zone, None)
        if bindings is None:
            bindings = dict()
            self._bindings[zone] = bindings

        if key in bindings.keys():
            return bindings[key]
        else:
            binding = Keybinding(key)
            bindings[key] = binding
            return binding

    @staticmethod
    def is_key_pressed(key: str) -> bool:
        return keyboard.is_pressed(key)

    def _on_press_key(self, event: keyboard.KeyboardEvent):
        for zone in self._bindings.values():
            for binding in zone.values():
                if binding.key == event.name:
                    binding.invoke_press(self.buffer)

        self.process_unbinds()

    def _on_release_key(self, event: keyboard.KeyboardEvent):
        for zone in self._bindings.values():
            for binding in zone.values():
                if binding.key == event.name:
                    binding.invoke_release(self.buffer)

        self.process_unbinds()
