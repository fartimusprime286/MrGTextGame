import datetime

from core.game import Scene


class SharedData:
    player_cell_scene: Scene
    hallway_scene: Scene
    bill_cell_scene: Scene
    current_date = datetime.date(2134, 1, 1)