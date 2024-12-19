from typing import cast

from core import Vec2, DefaultColors
from core.game import ObjectBehavior, Collider, GameObject
from core.konsole import KonsoleBuffer


class Inventory:
    items: list[str] = []

    @staticmethod
    def add_item(item: str):
        Inventory.items.append(item)

    @staticmethod
    def has_item(item: str) -> bool:
        return item in Inventory.items

class InventoryBehavior(ObjectBehavior):
    ITEM_BG_TEXTURE = "texture/textbox"
    ITEM_SELECT_COLOR = DefaultColors.BLUE.value
    SELECT_OFFSET = Vec2(0, -3)
    ITEM_BG_SIZE = Vec2(14, 7)
    ITEM_SIZE = Vec2(10, 5)
    ITEM_OFFSET = Vec2(2, 1)

    def __init__(self):
        super().__init__()
        self._selected_item = 0

    def on_load(self, buffer: KonsoleBuffer):
        pass

    def update(self, buffer: KonsoleBuffer):
        pass

    def render(self, buffer: KonsoleBuffer):
        items = Inventory.items
        len_items = len(items)
        if len_items > 4:
            if self._selected_item + 4 < len_items:
                items = Inventory.items[self._selected_item:self._selected_item + 4]
            else:
                items = Inventory.items[self._selected_item:]

        parent = cast(GameObject, self._parent)
        pos = parent.pos
        offset = Vec2(0, 0)
        for item_idx in range(len(items)):
            item = items[item_idx]
            item_texture = f"texture/item/{item}"
            buffer.draw_texture(
                pos + offset,
                InventoryBehavior.ITEM_BG_SIZE,
                InventoryBehavior.ITEM_BG_TEXTURE,
                False
            )

            buffer.draw_texture(
                pos + offset + InventoryBehavior.ITEM_OFFSET,
                InventoryBehavior.ITEM_SIZE,
                item_texture,
                False
            )

            if item_idx == self._selected_item:
                buffer.draw_rect(
                    pos + offset + InventoryBehavior.SELECT_OFFSET,
                    Vec2(InventoryBehavior.ITEM_BG_SIZE.x, 1),
                    False,
                    InventoryBehavior.ITEM_SELECT_COLOR
                )

            offset += Vec2(InventoryBehavior.ITEM_BG_SIZE.x + InventoryBehavior.ITEM_OFFSET.x, 0)




    def while_colliding(self, other: Collider):
        pass