class Inventory:
    items: list[str] = []

    @staticmethod
    def add_item(item: str) -> None:
        Inventory.items.append(item)