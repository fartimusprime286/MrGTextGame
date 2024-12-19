from datetime import datetime, date

from core.game import Collider, SceneKonsoleBuffer
from core.konsole import KonsoleBuffer
from core.text import TextRoot, TextNode
from data import SharedData
from game.behavior.psuedoinv import Inventory
from game.behavior.text import BaseTalkingCharacterBehavior
from game.character import CharacterFavorability


class Gretchen(BaseTalkingCharacterBehavior):
    date_list: list[date] = []

    def create_text(self, buffer: SceneKonsoleBuffer) -> TextRoot:
        def modify_favorability(favorability: int):
            CharacterFavorability.add_favorability("gretchen", favorability)

        def award_knife():
            Inventory.add_item("knife")

        #if you've already gotten food today, she'll refuse to give you anymore
        if SharedData.current_date in Gretchen.date_list:
            root = (TextRoot("Come back another day kid.\n(Gretchen's favorability towards you has fallen)")
                    .with_action(lambda obj, buf: modify_favorability(-5)))
            return root

        #If gretchen favors you, she'll offer you a knife, if you decline she'll favor you drastically less
        if CharacterFavorability.favorability_exceeds_threshold("gretchen", 30):
            root = TextRoot("Hey kid I got something for you.")
            root.add_child(TextNode(
                "Don't let the world stop ya kid.\n(Acquired knife)",
                "accept",
                lambda obj, buf: award_knife()
            )).add_child(TextNode(
                "Tch, you really just\ndon't got what it takes do ya.\n(Gretchen's favorability towards you has fallen massively)",
                "reject",
                lambda obj, buf: modify_favorability(-130)
            ))
        #Otherwise display regular dialog options
        else:
            root = TextRoot("Take yer pick and move along")
            root.add_child(TextNode(
                "What a fine choice.\n(Gretchen's favorability towards you has risen)",
                "slop",
                lambda obj, buf: modify_favorability(10)
            )).add_child(TextNode(
                "What kinda ditch did you crawl out of?\n(Gretchen's favorability towards you has fallen)",
                "better looking slop",
                lambda obj, buf: modify_favorability(-10)
            ))

        return root

    def character(self, buffer: SceneKonsoleBuffer) -> str:
        return "gretchen"

    def interaction_name(self) -> str:
        return f"talk to Gretchen (Favorability: {CharacterFavorability.favorability("gretchen")})"

    def on_load(self, buffer: KonsoleBuffer):
        pass

    def update(self, buffer: KonsoleBuffer):
        pass

    def render(self, buffer: KonsoleBuffer):
        pass

    def while_colliding(self, other: Collider):
        pass