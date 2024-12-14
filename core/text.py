from typing import Self


class TextNode:
    def __init__(self, text: str, option_name: str):
        self.text = text
        self.option_text = option_name
        self._children: list[TextNode] = []

    def add_child(self, child: Self) -> Self:
        self._children.append(child)
        return self

    def children(self) -> list[Self]:
        return self._children

class TextRoot(TextNode):
    def __init__(self, text: str):
        super().__init__(text, "root")
        self.text = text
        self._children: list[TextNode] = []

    def add_child(self, child: TextNode) -> Self:
        self._children.append(child)
        return self

    def children(self) -> list[TextNode]:
        return self._children
