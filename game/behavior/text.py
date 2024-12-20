from abc import ABC, abstractmethod, abstractproperty
from math import ceil
from typing import cast

from core import Vec2, DefaultColors
from core.behavior import Interactable
from core.game import ObjectBehavior, GameObject, SceneKonsoleBuffer, Collider
from core.input import InputHandler
from core.konsole import KonsoleBuffer
from core.text import TextRoot, TextNode
from data import SharedData


class TextBoxBehavior(ObjectBehavior):
    def __init__(self, text: TextRoot, person : str, character_size: Vec2 = Vec2(32, 16)):
        super().__init__()
        self.person = person
        self._character_size = character_size
        self._node: TextNode = text
        self._selected_option = 0
        self._key_zone = f"TextBox_{id(self)}"

    def on_load(self, buffer: KonsoleBuffer):
        parent = cast(GameObject, self._parent)
        scene_buffer = cast(SceneKonsoleBuffer, parent.scene)

        self._parent.is_raycast_collidable = False
        InputHandler.instance.get_or_create_keybind("up", self._key_zone).on_press(lambda _: self._scroll_up())
        InputHandler.instance.get_or_create_keybind("down", self._key_zone).on_press(lambda _: self._scroll_down())
        InputHandler.instance.get_or_create_keybind("enter", self._key_zone).on_press(lambda buf: self._climbtree(buf))
        SharedData.disable_player_controls = True

        self._node.on_selected(parent, scene_buffer)

    def update(self, buffer: KonsoleBuffer):
        pass

    def on_removed(self, buffer: KonsoleBuffer):
        InputHandler.instance.unbind_zone(self._key_zone)
        SharedData.disable_player_controls = False

    def _scroll_up(self):
        self._selected_option = max(0, self._selected_option - 1)

    def _scroll_down(self):
        self._selected_option = min(len(self._node.children()) - 1, self._selected_option + 1)

    def _climbtree(self, buffer: SceneKonsoleBuffer):
        parent = cast(GameObject, self._parent)
        scene_buffer = cast(SceneKonsoleBuffer, parent.scene)

        if len(self._node.children()) == 0:
            buffer.scene().remove_object(self._parent.name)
            return

        child = self._node.children()[self._selected_option]
        self._node = child
        self._selected_option = 0
        self._node.on_selected(parent, scene_buffer)

    def _render_text_centered(self, text: str, pos: Vec2, buffer: KonsoleBuffer):
        lines = text.splitlines()
        dy = ceil(len(lines) / 2)
        for i in range(len(lines)):
            line = lines[i]
            dx = ceil(len(line) / 2)
            buffer.draw_text(
                pos - Vec2(dx,dy-i), line ,
                True, len(line), False, draw_offsetted=False,
                color_mapper=lambda _: DefaultColors.BLACK.value,
                bg_color_mapper=lambda _: DefaultColors.WHITE.value
            )

    def _render_option(self, option: TextNode, offset: Vec2, buffer: KonsoleBuffer):
        if option not in self._node.children(): return

        idx = self._node.children().index(option)
        true_center = self._parent.pos + Vec2(self._parent.size.x/2, self._parent.size.y) + offset
        size = (self._parent.size / Vec2(1, 2)) - Vec2(4, 0)
        buffer.draw_texture(true_center - Vec2(size.x/2, 0), size, "texture/textbox", False)
        self._render_text_centered(option.option_text, true_center + Vec2(0, size.y / 2), buffer)
        if idx == self._selected_option:
            rect_pos = self._parent.pos + Vec2(0, self._parent.size.y) + offset
            buffer.draw_rect(rect_pos, Vec2(2, self._parent.size.y / 2), False, DefaultColors.RED.value)

    def render(self, buffer: KonsoleBuffer):
        sizething = self._parent.size - Vec2(self._character_size.x,0)
        center = self._parent.pos + Vec2(self._character_size.x, 0) + (sizething / Vec2(2,2))
        buffer.draw_texture(self._parent.pos, self._character_size, self.person, False)
        buffer.draw_texture(self._parent.pos + Vec2(self._character_size.x,0), sizething, draw_offsetted=False, texture_id="texture/textbox")
        self._render_text_centered(self._node.text, center, buffer)

        children = self._node.children()
        len_c = len(children)
        if len_c > 2:
            if self._selected_option + 2 < len_c:
                children = children[self._selected_option:self._selected_option+2]
            else:
                children = children[self._selected_option:]

        y_off = 2
        for child in children:
            self._render_option(child, Vec2(0, y_off), buffer)
            y_off += (self._parent.size.y / 2) + 2

    def while_colliding(self, other: Collider):
        pass


class BaseTalkingCharacterBehavior(Interactable, ABC):
    @abstractmethod
    def create_text(self, buffer: SceneKonsoleBuffer) -> TextRoot:
        pass

    @abstractmethod
    def character(self, buffer: SceneKonsoleBuffer) -> str:
        pass

    def character_size(self, buffer: SceneKonsoleBuffer) -> Vec2:
        return Vec2(32, 16)

    def textbox_pos(self, buffer: SceneKonsoleBuffer) ->  Vec2:
        return Vec2(100, 0)

    def textbox_size(self, buffer: SceneKonsoleBuffer) -> Vec2:
        return Vec2(100, 16)

    def character_texture_prepend(self, buffer: SceneKonsoleBuffer) -> str:
        return "texture/character"

    def on_interact(self, buffer: KonsoleBuffer, interaction_data):
        scene_buffer = cast(SceneKonsoleBuffer, buffer)
        text_root = self.create_text(scene_buffer)
        textbox_object = GameObject(
            f"text_box_{id(text_root)}",
            self.textbox_pos(scene_buffer),
            self.textbox_size(scene_buffer),
            TextBoxBehavior(
                text_root,
                f"{self.character_texture_prepend(scene_buffer)}/{self.character(scene_buffer)}",
                self.character_size(scene_buffer)
            )
        )

        scene_buffer.scene().add_object(textbox_object)

