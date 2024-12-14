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
        self._bindings: dict[str, Keybinding] = dict()
        keyboard.on_press(self._on_press_key)
        keyboard.on_release(self._on_release_key)
        InputHandler.instance = self

    @staticmethod
    def create(buffer: SceneKonsoleBuffer):
        if InputHandler.instance is not None:
            return InputHandler.instance
        else: return InputHandler(buffer)

    def get_or_create_keybind(self, key: str) -> Keybinding:
        if key in self._bindings.keys():
            return self._bindings[key]
        else:
            binding = Keybinding(key)
            self._bindings[key] = binding
            return binding

    @staticmethod
    def is_key_pressed(key: str) -> bool:
        return keyboard.is_pressed(key)

    def _on_press_key(self, event: keyboard.KeyboardEvent):
        for binding in self._bindings.values():
            if binding.key == event.name:
                binding.invoke_press(self.buffer)

    def _on_release_key(self, event: keyboard.KeyboardEvent):
        for binding in self._bindings.values():
            if binding.key == event.name:
                binding.invoke_release(self.buffer)

