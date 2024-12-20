import winsound

from datetime import date, timedelta, datetime
from typing import cast

from core.behavior import Interactable
from core.game import Collider, SceneKonsoleBuffer
from core.konsole import KonsoleBuffer
from core.text import TextRoot, TextNode
from data import SharedData
from game.behavior.text import BaseTalkingCharacterBehavior
from game.character import CharacterFavorability
from game.inventory import Inventory


class Gretchen(BaseTalkingCharacterBehavior):
    date_list: list[date] = []

    def create_text(self, buffer: SceneKonsoleBuffer) -> TextRoot:
        def modify_favorability(favorability: int):
            CharacterFavorability.add_favorability("gretchen", favorability)
            Gretchen.date_list.append(SharedData.current_date.date())

        def award_knife():
            Inventory.add_item("knife")
            Gretchen.date_list.append(SharedData.current_date.date())

        #if you've already gotten food today, she'll refuse to give you anymore
        if SharedData.current_date.date() in Gretchen.date_list:
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
        buffer.draw_texture(self._parent.pos, self._parent.size, "texture/character/standing/gretchen")

    def while_colliding(self, other: Collider):
        pass

class GretchenProxyBehavior(Interactable):
    def on_interact(self, buffer: KonsoleBuffer, interaction_data):
        scene_buffer = cast(SceneKonsoleBuffer, buffer)
        gretchen = scene_buffer.scene().get_object("gretchen")
        if gretchen is None:
            return

        candidates = gretchen.get_behavior_by_type(Gretchen)
        if len(candidates) == 0:
            return

        gretchen_behavior = candidates[0]
        gretchen_behavior.on_interact(buffer, interaction_data)

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

class Geff(BaseTalkingCharacterBehavior):
    date_list: list[date] = []

    def create_text(self, buffer: SceneKonsoleBuffer) -> TextRoot:
        def modify_favorability(favorability: int):
            CharacterFavorability.add_favorability("geff", favorability)

        def award_random_item():
            if SharedData.current_date <= datetime(2133,3,31) and SharedData.current_date >= datetime(1,1,1):
                Inventory.add_item("paper_airplane")
                for i in range(0,90):
                    Geff.date_list.append(date(2133,1,1) + timedelta(days=i))
            if SharedData.current_date <= datetime(2133,6,30) and SharedData.current_date >= datetime(2133,4,1):
                Inventory.add_item("lint")
                for i in range(0,91):
                    Geff.date_list.append(date(2133,4,1) + timedelta(days=i))
            if SharedData.current_date <= datetime(2133,9,30) and SharedData.current_date >= datetime(2133,7,1):
                Inventory.add_item("uncharged_gun")
                for i in range(0,92):
                    Geff.date_list.append(date(2133,7,1) + timedelta(days=i))
            if SharedData.current_date <= datetime(2133,12,31) and SharedData.current_date >= datetime(2133,10,1):
                Inventory.add_item("teddy_bear")
                for i in range(0,92):
                    Geff.date_list.append(date(2133,10,1) + timedelta(days=i))
            if SharedData.current_date <= datetime(2134,3,31) and SharedData.current_date >= datetime(2134,1,1):
                Inventory.add_item("mysterious_liquid")
                for i in range(0,90):
                    Geff.date_list.append(date(2134,1,1) + timedelta(days=i))
            if SharedData.current_date <= datetime(2134,6,30) and SharedData.current_date >= datetime(2134,4,1):
                Inventory.add_item("whoopie_cushion")
                for i in range(0,91):
                    Geff.date_list.append(date(2134,4,1) + timedelta(days=i))
            if SharedData.current_date <= datetime(2134,9,30) and SharedData.current_date >= datetime(2134,7,1):
                Inventory.add_item("crowbar")
                for i in range(0,92):
                    Geff.date_list.append(date(2134,7,1) + timedelta(days=i))
            if SharedData.current_date <= datetime(9999,12,31) and SharedData.current_date >= datetime(2134,10,1):
                Inventory.add_item("ball")
                for i in range(0,92):
                    Geff.date_list.append(date(2134,10,1) + timedelta(days=i))


        if not CharacterFavorability.favorability_exceeds_threshold("geff", -10):
            exit("Shouldnt have messed with him... (Made Geff Mad Ending)")

        elif SharedData.current_date.date() in Geff.date_list:
            root = (TextRoot("Wait another three months bub. You've got " + str(9 + (
                CharacterFavorability.favorability("geff"))) + " more chances" "\n(Geff got a little more angry)")
                    .with_action(lambda obj, buf: modify_favorability(-1)))

        else:
            root = TextRoot("Want a free trinket?")
            root.add_child(TextNode(
                "Here you go!\n(Acquired item)",
                "Sure",
                lambda obj, buf: award_random_item()
            )).add_child(TextNode(
                "Alrighty then.",
                "I dont take things from strangers",
            ))

        return root

    def character(self, buffer: SceneKonsoleBuffer) -> str:
        return "geff"

    def interaction_name(self) -> str:
        return f"talk to Geff the Robo Guard"

    def on_load(self, buffer: KonsoleBuffer):
        pass

    def update(self, buffer: KonsoleBuffer):
        pass

    def render(self, buffer: KonsoleBuffer):
        buffer.draw_texture(self._parent.pos, self._parent.size, "texture/robo_geff")
        pass

    def while_colliding(self, other: Collider):
        pass

