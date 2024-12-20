from typing import cast

from core import Vec2
from core.game import Scene, GameObject, SceneKonsoleBuffer
from core.konsole import KonsoleBuffer
from core.text import TextRoot
from game.behavior import TextBoxBehavior
from game.behavior.scene import SceneSwapper
from game.inventory import Inventory


class OfficeGate(SceneSwapper):
    def __init__(self, scene: Scene, interact_name: str, player_obj_id: str, new_player_pos: Vec2):
        super().__init__(scene, interact_name, player_obj_id, new_player_pos)

    def on_interact(self, buffer: KonsoleBuffer, interaction_data):
        scene_buffer = cast(SceneKonsoleBuffer, buffer)

        if Inventory.has_item("key"):
            super().on_interact(buffer, interaction_data)
            return

        root = TextRoot("(Thinking) This door is locked,\nif only I had a key.")
        textbox_obj = GameObject(f"textbox_{id(root)}", Vec2(100, 0), Vec2(100, 16), TextBoxBehavior(root))
        scene_buffer.scene().add_object(textbox_obj)
