import datetime
from datetime import timedelta
from typing import cast

from core import Vec2, Direction, DefaultColors
from core.behavior import Interactable
from core.game import ObjectBehavior, GameObject, Collider, SceneKonsoleBuffer, Scene
from core.input import InputHandler
from core.konsole import KonsoleBuffer
from core.physix import RigidBody
from core.text import TextRoot
from data import SharedData
from game.behavior import TextBoxBehavior
from game.behavior.scene import SceneSwapper


class PlayerBehavior(ObjectBehavior):
    def __init__(self):
        super().__init__()
        self.facing = Direction.UP
        self._interaction_name: (str | None) = None
        InputHandler.instance.get_or_create_keybind("\\", "player").on_press(lambda buf: self._attempt_interact(buf))

    def on_load(self, buffer: KonsoleBuffer):
        pass

    def update(self, buffer: KonsoleBuffer):
        if SharedData.disable_player_controls:
            return

        parent = cast(GameObject, self._parent)
        movement_vec = Vec2(0, 0)
        scene_buffer = cast(SceneKonsoleBuffer, buffer)

        rigid_body = parent.get_behavior_by_type(RigidBody)[0]

        if InputHandler.instance.is_key_pressed("w"):
            movement_vec.y -= 1
        if InputHandler.instance.is_key_pressed("a"):
            movement_vec.x -= 1
        if InputHandler.instance.is_key_pressed("s"):
            movement_vec.y += 1
        if InputHandler.instance.is_key_pressed("d"):
            movement_vec.x += 1
        if InputHandler.instance.is_key_pressed("k"):
            buffer.set_scene(SharedData.casino_scene)
            SharedData.casino_scene.add_object(GameObject("player", Vec2(10, 10), Vec2(6, 6), PlayerBehavior(), RigidBody()))
        if InputHandler.instance.is_key_pressed("right"):
            if SharedData.current_date <= datetime.date(2135, 1, 1):
                SharedData.current_date += timedelta(days=1)
            else:
                scene_buffer = cast(SceneKonsoleBuffer, buffer)
                timemastertbox = TextRoot("You can travel that far forward!")
                scene_buffer.scene().add_object(GameObject("timemaster tbox", Vec2(115, 4), Vec2(0, 0),TextBoxBehavior(timemastertbox, Vec2(70, 16), "texture/ball")))

        if InputHandler.instance.is_key_pressed("left"):
            if SharedData.current_date >= datetime.date(2132, 12, 31):
                SharedData.current_date -= timedelta(days=1)
            else:
                scene_buffer = cast(SceneKonsoleBuffer, buffer)
                timemastertbox = TextRoot("You can travel that far backward!")
                scene_buffer.scene().add_object(GameObject("timemaster tbox", Vec2(115, 4), Vec2(0, 0),TextBoxBehavior(timemastertbox, Vec2(70, 16),"texture/ball")))
        rigid_body.velocity = movement_vec * Vec2(2, 1)

        self._update_facing(movement_vec)

        interactable = self._find_interaction(scene_buffer)
        if interactable is not None:
            self._interaction_name = interactable.interaction_name()
        else: self._interaction_name = None

        self._camera_track(scene_buffer)

    def _camera_track(self, buffer: SceneKonsoleBuffer) -> None:
        scene = buffer.scene()
        if not scene.is_large():
            buffer.offset = Vec2(0, 0)
            return

        true_center = buffer.max_offsetted_dimensions / Vec2(2, 2)
        player_pos = self._parent.pos
        delta = true_center - player_pos
        buffer.offset = delta

    def _update_facing(self, movement_vec: Vec2):
        if movement_vec.magnitude() == 0: return

        if movement_vec.x > 0:
            self.facing = Direction.RIGHT
        elif movement_vec.x < 0:
            self.facing = Direction.LEFT
        elif movement_vec.y > 0:
            self.facing = Direction.DOWN
        else:
            self.facing = Direction.UP

    def _find_interaction(self, buffer: SceneKonsoleBuffer) -> (Interactable | None):
        raycast = buffer.scene().raycast(
            self._parent.pos, self.facing.value / Vec2(4, 4),
            self._parent.size, 2,
            lambda obj: obj is not self._parent
        )

        rcast_object = raycast[0]
        if rcast_object is None: return None

        interactables = rcast_object.get_behavior_by_type(Interactable)
        if interactables:
            return interactables[0]

    def _attempt_interact(self, buffer: SceneKonsoleBuffer):
        if SharedData.disable_player_controls:
            return

        interactable = self._find_interaction(buffer)

        if interactable is not None:
            interactable.on_interact(buffer, None)

    def render(self, buffer: KonsoleBuffer):
        match self.facing:
            case Direction.UP:
                texture = "texture/player/back"
            case Direction.LEFT:
                texture = "texture/player/left"
            case Direction.RIGHT:
                texture = "texture/player/right"
            case _:
                texture = "texture/player/front"

        buffer.draw_texture(self._parent.pos, self._parent.size, texture)
        buffer.draw_text(Vec2(104, 4), f"Current Date: {SharedData.current_date.strftime("%B, %d, %Y")}", draw_offsetted=False, color_mapper=lambda _: DefaultColors.RED.value)
        if self._interaction_name is not None:
            buffer.draw_text(Vec2(104, 6), f"Press BACKSLASH to {self._interaction_name}", draw_offsetted=False, color_mapper=lambda _: DefaultColors.RED.value)

    def while_colliding(self, other: Collider):
        pass
    