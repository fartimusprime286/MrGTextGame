from typing import cast

from core import Vec2, DefaultColors
from core.game import ObjectBehavior, Collider, GameObject
from core.input import InputHandler
from core.konsole import KonsoleBuffer
from core.util import get_or_none
from data import SharedData


class Inventory:
    items: list[str] = ["knife", "crowbar"]

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
        self._key_zone = f"inventory_{id(self)}"

    def on_load(self, buffer: KonsoleBuffer):
        SharedData.disable_player_controls = True
        pass

    def update(self, buffer: KonsoleBuffer):
        InputHandler.instance.get_or_create_keybind("left", self._key_zone).on_press(lambda _: self._scroll_left())
        InputHandler.instance.get_or_create_keybind("right", self._key_zone).on_press(lambda _: self._scroll_right())

    def _scroll_left(self):
        self._selected_item = min(len(Inventory.items) - 1, self._selected_item + 1)

    def _scroll_right(self):
        self._selected_item = max(0, self._selected_item - 1)

    def on_removed(self, buffer: KonsoleBuffer):
        InputHandler.instance.unbind_zone(self._key_zone)
        SharedData.disable_player_controls = False

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

        for item_idx in range(4):
            item = get_or_none(items, item_idx)
            buffer.draw_texture(
                pos + offset,
                InventoryBehavior.ITEM_BG_SIZE,
                InventoryBehavior.ITEM_BG_TEXTURE,
                False
            )

            if item is None:
                offset += Vec2(InventoryBehavior.ITEM_BG_SIZE.x + InventoryBehavior.ITEM_OFFSET.x, 0)
                continue

            item_texture = f"texture/item/{item}"

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