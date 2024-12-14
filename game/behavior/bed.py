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
    def __init__(self):
        super().__init__()
        self._time = 0.0
        self._tbox_active = False

    def interaction_name(self) -> str:
        return "Sleep"

    def on_interact(self, buffer: KonsoleBuffer, interaction_data):
        SharedData.current_date += timedelta(days=1)
        scene_buffer = cast(SceneKonsoleBuffer, buffer)
        scene_buffer.scene().add_object(GameObject("bed_tbox", Vec2(100, 0) , Vec2(0, 0), TextBoxBehavior(TextRoot("You slept"), Vec2(70, 16), "texture/bed")))
        self._time = time.time()
        self._tbox_active = True


    def on_load(self, buffer: KonsoleBuffer):
        pass

    def update(self, buffer: KonsoleBuffer):
        scene_buffer = cast(SceneKonsoleBuffer, buffer)

        if time.time() - self._time > 2 and self._tbox_active:
            self._time = time.time()
            scene_buffer.scene().remove_object("bed_tbox")
            self._tbox_active = False

    def render(self, buffer: KonsoleBuffer):
        pass

    def while_colliding(self, other: Collider):
        pass