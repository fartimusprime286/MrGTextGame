from ctypes import cast

import core.util
from core import Vec2
from core.behavior import Interactable
from core.game import Collider, SceneKonsoleBuffer, GameObject
from core.konsole import KonsoleBuffer
from core.text import TextRoot, TextNode
from data import SharedData
from game.behavior.text import BaseTalkingCharacterBehavior, TextBoxBehavior
from game.inventory import Inventory

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

