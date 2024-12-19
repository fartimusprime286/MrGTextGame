import threading
import time

import winsound

from math import ceil
from typing import cast

from winsound import PlaySound

from core import Vec2, DefaultColors
from core.behavior import Interactable
from core.game import ObjectBehavior, GameObject, Collider, SceneKonsoleBuffer
from core.input import InputHandler
from core.konsole import KonsoleBuffer
from core.text import TextRoot, TextNode
from data import SharedData


class TextBoxBehavior(ObjectBehavior):
    def __init__(self, text: TextRoot, size: Vec2, person : str, character_size: Vec2 = Vec2(32, 16)):
        super().__init__()
        self.size = size
        self.person = person
        self._character_size = character_size
        self._node: TextNode = text
        self._selected_option = 0
        self._key_zone = f"TextBox_{id(self)}"

    def on_load(self, buffer: KonsoleBuffer):
        InputHandler.instance.get_or_create_keybind("up", self._key_zone).on_press(lambda _: self._scroll_up())
        InputHandler.instance.get_or_create_keybind("down", self._key_zone).on_press(lambda _: self._scroll_down())
        InputHandler.instance.get_or_create_keybind("enter", self._key_zone).on_press(lambda buf: self._climbtree(buf))
        SharedData.disable_player_controls = True
        pass

    def update(self, buffer: KonsoleBuffer):
        pass

    def _scroll_up(self):
        self._selected_option = max(0, self._selected_option - 1)

    def _scroll_down(self):
        self._selected_option = min(len(self._node.children()) - 1, self._selected_option + 1)

    def _climbtree(self, buffer: SceneKonsoleBuffer):
        if len(self._node.children()) == 0:
            buffer.scene().remove_object(self._parent.name)
            InputHandler.instance.unbind_zone(self._key_zone)
            SharedData.disable_player_controls = False
            return

        child = self._node.children()[self._selected_option]
        self._node = child

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
        true_center = self._parent.pos + Vec2(self.size.x/2, self.size.y) + offset
        size = (self.size / Vec2(1, 2)) - Vec2(4, 0)
        buffer.draw_texture(true_center - Vec2(size.x/2, 0), size, "texture/textbox", False)
        self._render_text_centered(option.option_text, true_center + Vec2(0, size.y / 2), buffer)
        if idx == self._selected_option:
            rect_pos = self._parent.pos + Vec2(0, self.size.y) + offset
            buffer.draw_rect(rect_pos, Vec2(2, self.size.y / 2), False, DefaultColors.RED.value)

    def render(self, buffer: KonsoleBuffer):
        sizething = self.size - Vec2(self._character_size.x,0)
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
            y_off += (self.size.y / 2) + 2

    def while_colliding(self, other: Collider):
        pass


class ExamplePersonBehavior(Interactable):
    def __init__(self):
        super().__init__()

    def on_load(self, buffer: KonsoleBuffer):
        pass

    def update(self, buffer: KonsoleBuffer):
        pass

    def render(self, buffer: KonsoleBuffer):
        pass

    def while_colliding(self, other: Collider):
        pass

    def on_interact(self, buffer: KonsoleBuffer, interaction_data):
        scene_buffer = cast(SceneKonsoleBuffer, buffer)
        ballguywords = TextRoot("Hello Mr. G our game is currently... \n Computing... \n 35.36% Complete \n What would you like to know? \n Arrow keys to scroll, enter to select")
        ballguywords.add_child(
            TextNode("The Tales of Geoffus: The Sequel, \n Prequel, and Original", "What is the game called?").add_child(TextNode("Thank you very much", "Wow, that name is awesome")).add_child(TextNode("Go away hater", "Wow, that name sucks"))
        )
        ballguywords.add_child(TextNode("Thank you so much", "This game is awsome"))
        ballguywords.add_child(
            TextNode("Excuse me? Why are you here??", "Why are you here?").add_child(TextNode("Oh, I am here to make ensure that \n the games text features are shown off", "Sorry, I didn't mean it rudely")).add_child(TextNode("OWW!!","*Punch it*"))
        )
        scene_buffer.scene().add_object(GameObject("ballman tbox", Vec2(100, 0), Vec2(0, 0), TextBoxBehavior(ballguywords, Vec2(100, 16), "texture/ball")))

    def interaction_name(self) -> str:
        return "talk to ball"

class WardenBehavior(Interactable):
    def __init__(self):
        super().__init__()

    def on_load(self, buffer: KonsoleBuffer):
        pass

    def update(self, buffer: KonsoleBuffer):
        pass

    def render(self, buffer: KonsoleBuffer):
        pass

    def while_colliding(self, other: Collider):
        pass

    def on_interact(self, buffer: KonsoleBuffer, interaction_data):
        scene_buffer = cast(SceneKonsoleBuffer, buffer)
        Wardenwords = TextRoot("Greeting Geoffus, I am Prime the warden of this prison.")
        Wardenwords.add_child(
            TextNode("Ive been here since prime fortnite... I remember those days. *sighs*", "How long have you worked here?"))
        scene_buffer.scene().add_object(GameObject("ballman tbox", Vec2(100, 0), Vec2(0, 0), TextBoxBehavior(Wardenwords, Vec2(100, 16), "texture/ball")))

    def interaction_name(self) -> str:
        return "talk to Warden"


