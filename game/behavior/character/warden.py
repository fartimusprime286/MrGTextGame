import core.util
from core.game import Collider, SceneKonsoleBuffer
from core.konsole import KonsoleBuffer
from core.text import TextRoot, TextNode
from data import SharedData
from game.behavior.text import BaseTalkingCharacterBehavior
from game.inventory import Inventory


class Warden(BaseTalkingCharacterBehavior):
    def create_text(self, buffer: SceneKonsoleBuffer) -> TextRoot:
        root = TextRoot("You really thought you could escape?")
        death = lambda obj, buf: core.util.terminate("WARDEN DEATH ENDING: You have died to the warden!")
        root.add_child(
            TextNode("Your impudence amazes me!", "Uhhhhhh... Yeah...").add_child(
                TextNode("What do you think that's gonna do?", "Point at him").add_child(
                    TextNode("", "Await death", death)
                )
            ).add_child(
                TextNode("I'll amuse you, why did it?", "Why did the chicken cross the road?").add_child(
                    TextNode("This will be your last mistake", "To run away from your ugly face!").add_child(
                        TextNode("", "Await death", death)
                    )
                ).add_child(
                    TextNode("BAHAHAHAHAHAHAH! Good one talking about yourself.", "To escape from jail.").add_child(
                        TextNode("Fine, give it another go.", "That wasn't even my best joke\nlet me have another go").add_child(
                            TextNode("Who's there", "Knock knock!").add_child(
                                TextNode(f"In the big {SharedData.current_date.strftime("%Y")}, really?", "YO MAMA!").add_child(
                                    TextNode("", "Await death", death)
                                )
                            ).add_child(
                                TextNode("Not even humorous!", "ME!").add_child(
                                    TextNode("", "Await death", death)
                                )
                            )
                        ).add_child(
                            TextNode("What?", "What do you call a pony with a cough?").add_child(
                                TextNode("BAHAHAHAHAHA! Again! Again!", "A little horse").add_child(
                                    TextNode("TELL ME! TELL ME!", "Well what did the shark say when\n he ate a clownfish?").add_child(
                                        TextNode("Doesn't even make sense, DIE!", "burger").add_child(
                                            TextNode("", "Await death", death)
                                        )
                                    ).add_child(
                                        TextNode("QUITE HUMOROUS!", "This tastes a little funny").add_child(
                                            TextNode("Hey, where are you going", "Dash past him").add_child(
                                                TextNode("", "TOO LATE SUCKER!", lambda obj, buf: core.util.terminate("BONUS ENDING: You laughed the warden away!"))
                                            )
                                        )
                                    )
                                ).add_child(
                                    TextNode("Yes?", "Is your refrigerator running?").add_child(
                                        TextNode("DIE!", "Then you better go catch it!").add_child(
                                            TextNode("", "Await death", death)
                                        )
                                    )
                                )
                            ).add_child(
                                TextNode("You said it wrong, DIE!", "A small horse").add_child(
                                    TextNode("", "Await death", death)
                                )
                            )
                        )
                    ).add_child(
                        TextNode("Then die!", "I don't got anymore jokes.").add_child(
                            TextNode("", "Await death", death)
                        )
                    )
                )
            )
        ).add_child(
            TextNode("", "Await death", death)
        )

        if not Inventory.has_item("charged_gun"):
            return root

        root.add_child(
            TextNode("Ouch! What the hell dude!", "Shoot him").add_child(
                TextNode("MAN THAT SERIOUSLY HURTS!", "Shoot him again!").add_child(
                    TextNode("STOP!", "Shoot him again!!").add_child(
                        TextNode("XP", "Shoot him again!!!").add_child(
                            TextNode("", "Escape past his dead body", lambda obj, buf: core.util.terminate("TRUE ENDING: Shot and killed the warden"))
                        ).add_child(
                            TextNode("DIE!", "Apologize").add_child(
                                TextNode("", "Await death", death)
                            )
                        )
                    ).add_child(
                        TextNode("DIE!", "Apologize").add_child(
                            TextNode("", "Await death", death)
                        )
                    )
                ).add_child(
                    TextNode("DIE!", "Apologize").add_child(
                        TextNode("", "Await death", death)
                    )
                )
            ).add_child(
                TextNode("DIE!", "Apologize").add_child(
                    TextNode("", "Await death", death)
                )
            )
        )

        return root

    def character(self, buffer: SceneKonsoleBuffer) -> str:
        return "warden"

    def interaction_name(self) -> str:
        return "talk to Warden"

    def on_load(self, buffer: KonsoleBuffer):
        pass

    def update(self, buffer: KonsoleBuffer):
        pass

    def render(self, buffer: KonsoleBuffer):
        buffer.draw_texture(self._parent.pos, self._parent.size, "texture/character/standing/warden")

    def while_colliding(self, other: Collider):
        pass