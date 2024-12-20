from typing import cast

from core import Vec2
from core.behavior import Interactable
from core.game import GameObject, Collider, SceneKonsoleBuffer
from core.konsole import KonsoleBuffer
from core.text import TextRoot, TextNode
from game.behavior.text import TextBoxBehavior


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
        scene_buffer.scene().add_object(GameObject("ballman_tbox", Vec2(100, 0), Vec2(100, 16), TextBoxBehavior(ballguywords, "texture/ball", Vec2(32, 16))))

    def interaction_name(self) -> str:
        return "talk to ball"
