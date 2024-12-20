from datetime import datetime
from typing import cast

from PIL.ImageStat import Global

from core import Vec2
from core.behavior import Interactable
from core.game import GameObject, Collider, SceneKonsoleBuffer
from core.konsole import KonsoleBuffer
from core.text import TextRoot, TextNode
from data import SharedData
from game.behavior.scene import SceneSwapper
from game.behavior.text import TextBoxBehavior

UsedRoulette = 0
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


class RouletteBehavior(Interactable):
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
        global UsedRoulette
        def modify_UsedRoulette(e):
            global UsedRoulette
            UsedRoulette += e
        def Player_cell_teleport():
            SceneSwapper(SharedData.player_cell_scene, "go to player cell", "player", Vec2(40, 20))
        if SharedData.current_date > datetime(2134, 1, 1, hour=15, minute=30):
            if UsedRoulette == 0:
                roulettefeedback = TextRoot("Would you like to play roulette? \n Arrow keys to scroll, enter to select")
                roulettefeedback.add_child(
                    TextNode("Dang it landed red better luck next time", "Yes (Put everything on black").add_child(TextNode("(Thinking) Im upset now lets go back a couple minutes \n Use <- to go to the past \n Use -> to go to the future", "Leave", lambda obj, buf: modify_UsedRoulette(1))))

                roulettefeedback.add_child(TextNode("Dang it landed red better luck next time", "Definitely (Put everything on black").add_child(TextNode(
                    "(Thinking) Im upset now lets go back a couple minutes \n Use <- to go to the past \n Use -> to go to the future",
                    "Leave", lambda obj, buf: modify_UsedRoulette(1))))
                roulettefeedback.add_child(TextNode("Dang it landed red better luck next time", "Absolutely (Put everything on black").add_child(TextNode("(Thinking) Im upset now lets go back a couple minutes \n Use <- to go to the past \n Use -> to go to the future", "Leave", lambda obj, buf: modify_UsedRoulette(1))))
                scene_buffer.scene().add_object(GameObject("roulette_tbox", Vec2(100, 0), Vec2(100, 16), TextBoxBehavior(roulettefeedback, "texture/roulette_table")))
            else:
                roulettefeedback = TextRoot("(Thinking) Let me rewind first \n Remember \n Use <- to go to the past \n Use -> to go to the future")
                scene_buffer.scene().add_object(GameObject("roulette_tbox", Vec2(100, 0), Vec2(100, 16), TextBoxBehavior(roulettefeedback, "texture/roulette_table")))
        else:
            roulettefeedback = TextRoot("Would you like to play roulette? \n Arrow keys to scroll, enter to select")
            roulettefeedback.add_child(
                TextNode("You have been caught cheating Geoffus", "Yes (Play red").add_child(TextNode("You are now imprisoned for you entire meaningless lifetime","Oh no").add_child(TextNode("(Thinking) I can't stay here forever, i have to use my powers to escape \n I can now travel in days but only up to a year", "", lambda obj, buf: Player_cell_teleport()))))
            scene_buffer.scene().add_object(GameObject("roulette_tbox", Vec2(100, 0), Vec2(100, 16), TextBoxBehavior(roulettefeedback, "texture/police")))

    def interaction_name(self) -> str:
        return "use roulette table"



