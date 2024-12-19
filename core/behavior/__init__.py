from abc import ABC, abstractmethod

import core.logging
from core.game import ObjectBehavior, Collider
from core.konsole import KonsoleBuffer


class Textured(ObjectBehavior):
    def __init__(self, texture_id: str, ui: bool = False):
        super().__init__()
        self.texture_id = texture_id
        self.ui = ui

    def on_load(self, buffer: KonsoleBuffer):
        pass

    def update(self, buffer: KonsoleBuffer):
        pass

    def render(self, buffer: KonsoleBuffer):
        #core.logging.debug(f"drawing obj: {self._parent.name}, size: {self._parent.size}, texture {self.texture_id}")
        buffer.draw_texture(self._parent.pos, self._parent.size, self.texture_id, not self.ui)

    def while_colliding(self, other: Collider):
        pass

class Interactable(ObjectBehavior, ABC):
    @abstractmethod
    def on_interact(self, buffer: KonsoleBuffer, interaction_data):
        pass

    @abstractmethod
    def interaction_name(self) -> str:
        pass