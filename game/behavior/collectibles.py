from typing import cast

from core.behavior import Interactable
from core.game import Collider, SceneKonsoleBuffer
from core.konsole import KonsoleBuffer
from game.inventory import Inventory


class Collectible(Interactable):
    def __init__(self, collectible_name: str, texture: (str | None) = None):
        super().__init__()
        self.item = collectible_name
        if texture is not None:
            self._texture = texture
        else:
            self._texture = f"texture/item/{self.item}"

    def on_interact(self, buffer: KonsoleBuffer, interaction_data):
        scene_buffer = cast(SceneKonsoleBuffer, buffer)
        Inventory.add_item(self.item)
        scene_buffer.scene().remove_object(self._parent.name)

    def interaction_name(self) -> str:
        return f"pick up {self.item}"

    def on_load(self, buffer: KonsoleBuffer):
        pass

    def update(self, buffer: KonsoleBuffer):
        pass

    def render(self, buffer: KonsoleBuffer):
        buffer.draw_texture(self._parent.pos, self._parent.size, self._texture)

    def while_colliding(self, other: Collider):
        pass