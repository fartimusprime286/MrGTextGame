import time
from datetime import timedelta
from typing import cast

from core import Vec2
from core.behavior import Interactable
from core.game import Collider, SceneKonsoleBuffer, GameObject
from core.text import TextRoot
from game.behavior import TextBoxBehavior
from data import SharedData
from core.konsole import KonsoleBuffer


class BedBehavior(Interactable):
    def interaction_name(self) -> str:
        return "Sleep"

    def on_interact(self, buffer: KonsoleBuffer, interaction_data):
        SharedData.current_date += timedelta(days=1)
        scene_buffer = cast(SceneKonsoleBuffer, buffer)
        scene_buffer.scene().add_object(GameObject("bed_tbox", Vec2(100, 0) , Vec2(0, 0), TextBoxBehavior(TextRoot("You slept"), Vec2(100, 16), "texture/bed", Vec2(16, 16))))

    def on_load(self, buffer: KonsoleBuffer):
        pass

    def update(self, buffer: KonsoleBuffer):
        pass

    def render(self, buffer: KonsoleBuffer):
        pass

    def while_colliding(self, other: Collider):
        pass