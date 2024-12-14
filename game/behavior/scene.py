from typing import cast

from core import Vec2
from core.behavior import Interactable
from core.game import Collider, SceneKonsoleBuffer, Scene
from core.konsole import KonsoleBuffer


class SceneSwapper(Interactable):
    def __init__(self, scene: Scene, interact_name: str, player_obj_id: str, new_player_pos: Vec2):
        super().__init__()
        self.scene = scene
        self.player_obj_id = player_obj_id
        self.new_player_pos = new_player_pos
        self.interact_name = interact_name

    def on_interact(self, buffer: KonsoleBuffer, interaction_data):
        scene_buffer = cast(SceneKonsoleBuffer, buffer)
        player = scene_buffer.scene().remove_object(self.player_obj_id)
        self.scene.add_object(player)
        scene_buffer.set_scene(self.scene)
        player.pos = self.new_player_pos

    def interaction_name(self) -> str:
        return self.interact_name

    def on_load(self, buffer: KonsoleBuffer):
        pass

    def update(self, buffer: KonsoleBuffer):
        pass

    def render(self, buffer: KonsoleBuffer):
        pass

    def while_colliding(self, other: Collider):
        pass