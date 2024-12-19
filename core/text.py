from typing import Self, Callable

from core.game import SceneKonsoleBuffer, GameObject


class TextNode:
    def __init__(self, text: str, option_name: str, action: Callable[[GameObject, SceneKonsoleBuffer], None] = lambda obj, buf: None):
        self.text = text
        self.option_text = option_name
        self._children: list[TextNode] = []
        self._action: Callable[[GameObject, SceneKonsoleBuffer], None] = action

    def with_action(self, action: Callable[[GameObject, SceneKonsoleBuffer], None] = lambda: None) -> Self:
        self._action = action
        return self

    def add_child(self, child: Self) -> Self:
        self._children.append(child)
        return self

    def children(self) -> list[Self]:
        return self._children

    def on_selected(self, game_object: GameObject, buffer: SceneKonsoleBuffer):
        self._action(game_object, buffer)


class TextRoot(TextNode):
    def __init__(self, text: str):
        super().__init__(text, "root")

    def add_child(self, child: TextNode) -> Self:
        self._children.append(child)
        return self

    def children(self) -> list[TextNode]:
        return self._children

#blah = TextRoot("blah")
#, event: Callable[[Self], None]