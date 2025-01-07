from datetime import datetime
from logging import root
from typing import cast

from PIL.ImageStat import Global

import core

from core import Vec2
from core.behavior import Interactable, Textured
from core.game import GameObject, Collider, SceneKonsoleBuffer
from core.konsole import KonsoleBuffer
from core.physix import RigidBody
from core.text import TextRoot, TextNode

from data import SharedData
from game.behavior.text import TextBoxBehavior
from game.behavior.player import PlayerBehavior
from game.behavior.scene import SceneSwapper
from game.inventory import Inventory


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
        def tutorial_complete():
            SceneSwapper(SharedData.player_cell_scene, "go to player cell", "player", Vec2(20, 10)).on_interact(scene_buffer, None)
        if SharedData.current_date > datetime(2134, 1, 1, hour=15, minute=29):
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
                TextNode("You have been caught cheating Geoffus", "Yes (Play red)").add_child(TextNode("You are now imprisoned for the rest \n of your entire meaningless life","Oh no").add_child(TextNode("(Thinking) I can't stay here forever, \n i have to use my powers to escape \n I can now travel in days but only up to a year", "", lambda obj, buf: tutorial_complete()))))
            scene_buffer.scene().add_object(GameObject("roulette_tbox", Vec2(100, 0), Vec2(100, 16), TextBoxBehavior(roulettefeedback, "texture/police")))

    def interaction_name(self) -> str:
        return "use roulette table"

class LucasBehavior(Interactable):
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
        death = lambda obj, buf: core.util.terminate("ERROR IN JUDGEMENT ENDING: You have died to the lucas! \n you idiot")
        lucaswords = TextRoot("Hey bud")
        lucaswords.add_child(
            TextNode("Im lucas been here for a couple years now", "who are you?")
            .add_child(TextNode("Yup", "Wow, that's a long time"))
        )
        lucaswords.add_child(TextNode("Not really but i do know quite a bit about this place", "You know anything about escaping this place?").add_child(TextNode("That's bills cell  \n probably was your best chance at escaping \n too bad he died a couple months ago", "Know anything about that empty cell across from mine?")
        .add_child(TextNode("...", "What about that joel fellow across from your cell?")
        .add_child(TextNode("I hear he can give you different items depending on the month", "Know anything about jeff?")))))
        lucaswords.add_child(TextNode("You will regret this","*Punch him*", death))
        lucaswords.add_child(TextNode("bye","Goodbye"))
        scene_buffer.scene().add_object(GameObject("Lucas_tbox", Vec2(100, 0), Vec2(100, 16), TextBoxBehavior(lucaswords, "texture/lucas_talking", Vec2(32, 16))))

    def interaction_name(self) -> str:
        return "talk to Lucas"

class Bill_Summoner(SceneSwapper):
    BillsTime = datetime(2133, 9, 1, 15)

    def on_interact(self, buffer: KonsoleBuffer, interaction_data):
        scene_buffer = cast(SceneKonsoleBuffer, buffer)

        if SharedData.current_date < Bill_Summoner.BillsTime:
            SharedData.bill_cell_scene.add_object(GameObject("Bill", Vec2(20, 25), Vec2(10, 10), Textured("texture/bill_front"),BillBehavior()))
            super().on_interact(buffer, interaction_data)
        else:
            super().on_interact(buffer, interaction_data)

class BillBehavior(Interactable):
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
        billwords = TextRoot("Hey punk")
        billwords.add_child(
            TextNode("Yeah what is it to you?", "You bill?").add_child(TextNode("Don't know if i can trust you", "I gotta know how your escaping").add_child(TextNode("Alright fine you got me \n Im planning to escape through a vent in the showers \n which you can unscrew with a knife \n only problem is to get the knife \n your gonna need a good relationship with gretchen \n you'll also need a crowbar from jeff", "pretty please (:"))
        ))
        billwords.add_child(TextNode("The only way to survive in this place", "Why so rude?"))
        billwords.add_child(TextNode("hot belgium waffles","*Punch him*"))
        billwords.add_child(TextNode("bye","Goodbye"))
        scene_buffer.scene().add_object(GameObject("Bill_tbox", Vec2(100, 0), Vec2(100, 16), TextBoxBehavior(billwords, "texture/bill_talking", Vec2(32, 16))))

    def interaction_name(self) -> str:
        return "talk to Bill"

class Prison_Gate(SceneSwapper):
    def on_interact(self, buffer: KonsoleBuffer, interaction_data):
        scene_buffer = cast(SceneKonsoleBuffer, buffer)
        root = TextRoot("")
        if Inventory.has_item("key"):
            super().on_interact(buffer, interaction_data)
        else:
            root.add_child(
                TextNode("Locked", "Unlock the gate"))
        textbox_obj = GameObject(f"textbox_{id(root)}", Vec2(100, 0), Vec2(100, 16), TextBoxBehavior(root))
        scene_buffer.scene().add_object(textbox_obj)







