import datetime

from core.game import Scene


class SharedData:
    disable_player_controls = False
    player_cell_scene: Scene
    hallway_scene: Scene
    bill_cell_scene: Scene
    hallway_second_scene: Scene
    joel_camilo_cell_scene: Scene
    lucas_julien_cerrato_cell_scene: Scene
    courtyard_scene: Scene
    cafeteria_scene: Scene
    showers_scene: Scene
    office_scene: Scene
    casino_scene: Scene
    current_date = datetime.date(2134, 1, 1)