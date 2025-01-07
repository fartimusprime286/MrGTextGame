from datetime import datetime
from typing import cast

from core import Vec2
from core.game import GameObject, SceneKonsoleBuffer, Scene
from core.konsole import KonsoleBuffer
from core.text import TextRoot, TextNode
from data import SharedData
from game.behavior import TextBoxBehavior
from game.behavior.scene import SceneSwapper
from game.inventory import Inventory



class ShowersGate(SceneSwapper):
    RENOVATIONS_END_DATE = datetime(2134, 4, 19, 12)

    def on_interact(self, buffer: KonsoleBuffer, interaction_data):
        scene_buffer = cast(SceneKonsoleBuffer, buffer)

        if SharedData.current_date > ShowersGate.RENOVATIONS_END_DATE:
            super().on_interact(buffer, interaction_data)
        else:
            root = TextRoot(f"Showers are currently under renovation,\nI hear renovations will be done by\n{ShowersGate.RENOVATIONS_END_DATE.strftime("%B %d, %Y, %H:%M")}.")
            textbox_obj = GameObject(f"textbox_{id(root)}", Vec2(100, 0), Vec2(100, 16), TextBoxBehavior(root))
            scene_buffer.scene().add_object(textbox_obj)

class Vent(SceneSwapper):
    def __init__(self, scene: Scene, interact_name: str, player_obj_id: str, new_player_pos: Vec2):
        super().__init__(scene, interact_name, player_obj_id, new_player_pos)
        self._is_open = False

    def on_interact(self, buffer: KonsoleBuffer, interaction_data):
        scene_buffer = cast(SceneKonsoleBuffer, buffer)

        if self._is_open:
            super().on_interact(buffer, interaction_data)
            return

        def open_vent():
            self._is_open = True

        root = TextRoot("This vent is closed.")
        if Inventory.has_item("knife"):
            if Inventory.has_item("crowbar"):
                root.add_child(TextNode("(Thinking) Managed to open it, cool", "Open the vent", lambda obj, buf: open_vent()))
            else:
                root.add_child(TextNode("(Thinking) This vent won't budge,\nif only I had a crowbar to pry it open", "Open the vent"))
        else:
            root.add_child(TextNode("(Thinking) These screws are sturdy,\nwish I had a knife", "Open the vent"))

        root.add_child(TextNode("(Thinking) Maybe I could've opened it", "Leave"))

        textbox_obj = GameObject(f"textbox_{id(root)}", Vec2(100, 0), Vec2(100, 16), TextBoxBehavior(root))
        scene_buffer.scene().add_object(textbox_obj)

