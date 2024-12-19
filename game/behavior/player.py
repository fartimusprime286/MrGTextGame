from datetime import timedelta, datetime
from typing import cast

from core import Vec2, Direction, DefaultColors
from core.behavior import Interactable
from core.game import ObjectBehavior, GameObject, Collider, SceneKonsoleBuffer
from core.input import InputHandler
from core.konsole import KonsoleBuffer
from core.physix import RigidBody
from core.text import TextRoot
from data import SharedData
from game.behavior import TextBoxBehavior
from game.inventory import InventoryBehavior


class PlayerBehavior(ObjectBehavior):
    def __init__(self):
        super().__init__()
        self.facing = Direction.UP
        self._interaction_name: (str | None) = None
        self._ticks_since_update_time = 0
        InputHandler.instance.get_or_create_keybind("\\", "player").on_press(lambda buf: self._attempt_interact(buf))
        InputHandler.instance.get_or_create_keybind("right", "player").on_press(lambda buf: self._travel_forwards(buf))
        InputHandler.instance.get_or_create_keybind("left", "player").on_press(lambda buf: self._travel_backwards(buf))
        InputHandler.instance.get_or_create_keybind("e", "player").on_press(lambda buf: self._open_inventory(buf))
        InputHandler.instance.get_or_create_keybind("escape", "player").on_press(lambda buf: self._close_inventory(buf))

    def on_load(self, buffer: KonsoleBuffer):
        pass

    def update(self, buffer: KonsoleBuffer):
        if SharedData.disable_player_controls:
            return

        self._ticks_since_update_time += 1
        if self._ticks_since_update_time >= 10:
            SharedData.current_date += timedelta(minutes=1)
            self._ticks_since_update_time = 0

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
            scene_buffer.set_scene(SharedData.casino_scene)
            SharedData.casino_scene.add_object(GameObject("player", Vec2(90, 30), Vec2(6, 6), PlayerBehavior(), RigidBody()))
        if InputHandler.instance.is_key_pressed("j"):
            scene_buffer.set_scene(SharedData.outside_scene)
            SharedData.outside_scene.add_object(GameObject("player", Vec2(90, 30), Vec2(6, 6), PlayerBehavior(), RigidBody()))


        rigid_body.velocity = movement_vec * Vec2(2, 1)

        self._update_facing(movement_vec)

        interactable = self._find_interaction(scene_buffer)
        if interactable is not None:
            self._interaction_name = interactable.interaction_name()
        else: self._interaction_name = None

        self._camera_track(scene_buffer)

    def _open_inventory(self, buffer: SceneKonsoleBuffer):
        buffer.scene().add_object(GameObject("inventory", Vec2(100, 96), Vec2(0, 0), InventoryBehavior()))

    def _close_inventory(self, buffer: SceneKonsoleBuffer):
        buffer.scene().remove_object("inventory")

    def _travel_forwards(self, buffer: SceneKonsoleBuffer):
        self._time_travel(buffer, True)

    def _travel_backwards(self, buffer: SceneKonsoleBuffer):
        self._time_travel(buffer, False)

    def _time_travel(self, buffer: SceneKonsoleBuffer, forwards: bool):
        if SharedData.disable_player_controls:
            return

        if forwards:
            if SharedData.current_date >= datetime(2132, 12, 31):
                SharedData.current_date -= timedelta(days=1)
            else:
                timemastertbox = TextRoot("You can't travel that far backward!")
                buffer.scene().add_object(GameObject("timemaster_tbox", Vec2(100, 0), Vec2(100, 16),TextBoxBehavior(timemastertbox,"texture/ball")))
        else:
            if SharedData.current_date <= datetime(2135, 1, 1):
                SharedData.current_date += timedelta(days=1)
            else:
                timemastertbox = TextRoot("You can't travel that far forward!")
                buffer.scene().add_object(GameObject("timemaster_tbox", Vec2(100, 0), Vec2(100, 16),TextBoxBehavior(timemastertbox, "texture/ball")))

    def _camera_track(self, buffer: SceneKonsoleBuffer) -> None:
        scene = buffer.scene()
        if not scene.is_large():
            buffer.offset = Vec2(0, 0)
            return

        true_center = buffer.max_offsetted_dimensions / Vec2(2, 2)
        player_pos = self._parent.pos
        delta = true_center - player_pos
        #core.logging.debug(f"DELTA: {delta}")
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

        if SharedData.disable_player_controls:
            return

        buffer.draw_text(Vec2(104, 4), f"Current Date: {SharedData.current_date.strftime("%B %d, %Y, %H:%M (%A)")}", draw_offsetted=False, color_mapper=lambda _: DefaultColors.RED.value)
        if self._interaction_name is not None:
            buffer.draw_text(Vec2(104, 6), f"Press BACKSLASH to {self._interaction_name}", draw_offsetted=False, color_mapper=lambda _: DefaultColors.RED.value)

    def while_colliding(self, other: Collider):
        pass
    