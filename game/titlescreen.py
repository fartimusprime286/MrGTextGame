from core import clamp, Vec2
from core.input import InputHandler
from core.game import ObjectBehavior, Collider, SceneKonsoleBuffer
from core.konsole import KonsoleBuffer


class TitleScreenBehavior(ObjectBehavior):
    def __init__(self):
        super().__init__()
        self.selected_option = 0

    def on_load(self, buffer: KonsoleBuffer):
        self.selected_option = 0
        def decrement_option(b: SceneKonsoleBuffer):
            self.selected_option = clamp(self.selected_option - 1, 0, 1)

        def increment_option(b: SceneKonsoleBuffer):
            self.selected_option = clamp(self.selected_option + 1, 0, 1)


        InputHandler.instance.get_or_create_keybind("left").on_press(decrement_option)
        InputHandler.instance.get_or_create_keybind("right").on_press(increment_option)
        InputHandler.instance.get_or_create_keybind("enter").on_press(self.on_enter)

    def on_enter(self, buffer: SceneKonsoleBuffer):
        if self.selected_option == 0:
            pass
        else:
            buffer.quit()



    def update(self, buffer: KonsoleBuffer):
        pass

    def render(self, buffer: KonsoleBuffer):
        if self.selected_option == 0:
            buffer.draw_texture(Vec2(19, 19), None, "button.active")
            buffer.draw_texture(Vec2(44, 19), None, "button.inactive")
        else:
            buffer.draw_texture(Vec2(19, 19), None, "button.inactive")
            buffer.draw_texture(Vec2(44, 19), None, "button.active")
        buffer.draw_text(Vec2(26, 21), "START")
        buffer.draw_text(Vec2(51, 21), "QUITS")

        pass

    def while_colliding(self, other: Collider):
        pass