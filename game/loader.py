import time
import winsound
from winsound import PlaySound

from core import Vec2
from core.behavior import Textured
from game.behavior.bed import BedBehavior
from game.behavior.scene import SceneSwapper
from core.physix import RigidBody
from game.behavior.player import PlayerBehavior
from core.game import GameLoader, SceneKonsoleBuffer, GameObject
from data import SharedData
from game.behavior import ExamplePersonBehavior


class PrisonGameLoader(GameLoader):
    def on_make_buffer(self, buffer: SceneKonsoleBuffer):


        #create player cell
        SharedData.player_cell_scene = buffer.create_scene()
        #create hallway scene - set_large enable pseudo- camera tracking
        SharedData.hallway_scene = buffer.create_scene().set_large()
        SharedData.hallway_second_scene = buffer.create_scene().set_large()
        SharedData.cafeteria_scene = buffer.create_scene().set_large()
        SharedData.bill_cell_scene = buffer.create_scene()
        SharedData.joel_camilo_cell_scene = buffer.create_scene()
        SharedData.lucas_julien_cerrato_cell_scene = buffer.create_scene()
        SharedData.courtyard_scene = buffer.create_scene()

        #player cell scene data
        SharedData.player_cell_scene.add_object(GameObject("roof", Vec2(0, 0), Vec2(100, 2), Textured("texture/floor")))
        SharedData.player_cell_scene.add_object(GameObject("left_wall", Vec2(0, 0), Vec2(2, 40), Textured("texture/wall")))
        SharedData.player_cell_scene.add_object(GameObject("right_wall", Vec2(98, 0), Vec2(2, 40), Textured("texture/wall")))

        #floor
        SharedData.player_cell_scene.add_object(GameObject("floor_l", Vec2(0, 38), Vec2(40, 2), Textured("texture/floor")))
        SharedData.player_cell_scene.add_object(
            GameObject(
                "gate", Vec2(40, 38), Vec2(20, 2),
                Textured("texture/gate"),
                SceneSwapper(SharedData.hallway_scene, "go to hallway", "player", Vec2(40, 10))
            )
        )
        SharedData.player_cell_scene.add_object(GameObject("floor_r", Vec2(60, 38), Vec2(40, 2), Textured("texture/floor")))

        SharedData.player_cell_scene.add_object(GameObject("player", Vec2(10, 10), Vec2(6, 6), PlayerBehavior(), RigidBody()))
        SharedData.player_cell_scene.add_object(GameObject("bed", Vec2(86, 3), Vec2(10, 10), Textured("texture/bed"), BedBehavior()))
        SharedData.player_cell_scene.add_object(GameObject("ball_person", Vec2(15, 30), Vec2(4, 4),Textured("texture/ball"),ExamplePersonBehavior()))

        #Hallway scene data

        #roof
        SharedData.hallway_scene.add_object(GameObject("roof_l", Vec2(0, 0), Vec2(40, 2), Textured("texture/floor") ))
        SharedData.hallway_scene.add_object(
            GameObject(
                "gate", Vec2(40, 0), Vec2(20, 2),
                Textured("texture/gate"),
                SceneSwapper(SharedData.player_cell_scene, "go to player cell","player", Vec2(40, 30))
            )
        )
        SharedData.hallway_scene.add_object(GameObject("roof_r", Vec2(60, 0), Vec2(40, 2), Textured("texture/floor")))

        SharedData.hallway_scene.add_object(GameObject("left_wall_up", Vec2(0, 0), Vec2(2, 10), Textured("texture/wall")))
        SharedData.hallway_scene.add_object(GameObject("left_wall_down", Vec2(0, 30), Vec2(2, 10), Textured("texture/wall")))
        SharedData.hallway_scene.add_object(
            GameObject(
                "hallway_gate", Vec2(0, 10), Vec2(2, 20),
                Textured("texture/gate"),
                SceneSwapper(SharedData.hallway_second_scene, "go to second hallway","player", Vec2(190, 25))
            )
        )
        SharedData.hallway_scene.add_object(GameObject("right_wall_up", Vec2(198, 0), Vec2(2, 10), Textured("texture/wall")))
        SharedData.hallway_scene.add_object(GameObject("right_wall_down", Vec2(198, 30), Vec2(2, 10), Textured("texture/wall")))
        SharedData.hallway_scene.add_object(
            GameObject(
                "courtyard_gate", Vec2(198, 10), Vec2(2, 20),
                Textured("texture/gate"),
                SceneSwapper(SharedData.courtyard_scene, "go to courtyard","player", Vec2(20, 25))
            )
        )
        SharedData.hallway_scene.add_object(GameObject("floor3_l", Vec2(100, 38), Vec2(40, 2), Textured("texture/floor")))
        SharedData.hallway_scene.add_object(
            GameObject(
                "gate_joel_camilo", Vec2(140, 38), Vec2(20, 2),
                Textured("texture/gate"),
                SceneSwapper(SharedData.joel_camilo_cell_scene, "go to joel camilos cell", "player", Vec2(40, 10))
            )
        )
        SharedData.hallway_scene.add_object(GameObject("floor3_r", Vec2(160, 38), Vec2(40, 2), Textured("texture/floor")))
        #SharedData.hallway_scene.add_object(GameObject("right_wall", Vec2(98, 0), Vec2(2, 40), Textured("texture/wall")))

        #floor
        SharedData.hallway_scene.add_object(GameObject("floor2_l", Vec2(0, 38), Vec2(40, 2), Textured("texture/floor")))
        SharedData.hallway_scene.add_object(
            GameObject(
                "gate_bill", Vec2(40, 38), Vec2(20, 2),
                Textured("texture/gate"),
                SceneSwapper(SharedData.bill_cell_scene, "go to bills cell", "player", Vec2(40, 10))
            )
        )
        SharedData.hallway_scene.add_object(GameObject("floor2_r", Vec2(60, 38), Vec2(40, 2), Textured("texture/floor")))

        SharedData.hallway_scene.add_object(GameObject("roof2_l", Vec2(100, 0), Vec2(40, 2), Textured("texture/floor") ))
        SharedData.hallway_scene.add_object(
            GameObject(
                "lucas_gate", Vec2(140, 0), Vec2(20, 2),
                Textured("texture/gate"),
                SceneSwapper(SharedData.lucas_julien_cerrato_cell_scene, "go to lucas julien cerrato cell","player", Vec2(40, 30))
            )
        )
        SharedData.hallway_scene.add_object(GameObject("roof2_r", Vec2(160, 0), Vec2(40, 2), Textured("texture/floor")))

        #Bill cell scene
        SharedData.bill_cell_scene.add_object(GameObject("roof", Vec2(0, 38), Vec2(100, 2), Textured("texture/floor")))
        SharedData.bill_cell_scene.add_object(GameObject("left_wall", Vec2(0, 0), Vec2(2, 40), Textured("texture/wall")))
        SharedData.bill_cell_scene.add_object(GameObject("right_wall", Vec2(98, 0), Vec2(2, 40), Textured("texture/wall")))
        SharedData.bill_cell_scene.add_object(GameObject("roof_l", Vec2(0, 0), Vec2(40, 2), Textured("texture/floor") ))
        SharedData.bill_cell_scene.add_object(
            GameObject(
                "gate_hallway_bill", Vec2(40, 0), Vec2(20, 2),
                Textured("texture/gate"),
                SceneSwapper(SharedData.hallway_scene, "go to hallway","player", Vec2(40, 30))
            )
        )
        SharedData.bill_cell_scene.add_object(GameObject("roof_r", Vec2(60, 0), Vec2(100, 2), Textured("texture/floor")))

        # lucas julien cerrato cell scene data
        SharedData.lucas_julien_cerrato_cell_scene.add_object(GameObject("roof", Vec2(0, 0), Vec2(100, 2), Textured("texture/floor")))
        SharedData.lucas_julien_cerrato_cell_scene.add_object(
            GameObject("left_wall", Vec2(0, 0), Vec2(2, 40), Textured("texture/wall")))
        SharedData.lucas_julien_cerrato_cell_scene.add_object(
            GameObject("right_wall", Vec2(98, 0), Vec2(2, 40), Textured("texture/wall")))

        # floor4
        SharedData.lucas_julien_cerrato_cell_scene.add_object(
            GameObject("floor4_l", Vec2(0, 38), Vec2(40, 2), Textured("texture/floor")))
        SharedData.lucas_julien_cerrato_cell_scene.add_object(
            GameObject(
                "gate_hallway_lucas", Vec2(40, 38), Vec2(20, 2),
                Textured("texture/gate"),
                SceneSwapper(SharedData.hallway_scene, "go to hallway", "player", Vec2(140, 10))
            )
        )
        SharedData.lucas_julien_cerrato_cell_scene.add_object(
            GameObject("floor4_r", Vec2(60, 38), Vec2(40, 2), Textured("texture/floor")))

        #Joel camillo cell scene
        SharedData.joel_camilo_cell_scene.add_object(GameObject("roof", Vec2(0, 38), Vec2(100, 2), Textured("texture/floor")))
        SharedData.joel_camilo_cell_scene.add_object(GameObject("left_wall", Vec2(0, 0), Vec2(2, 40), Textured("texture/wall")))
        SharedData.joel_camilo_cell_scene.add_object(GameObject("right_wall", Vec2(98, 0), Vec2(2, 40), Textured("texture/wall")))
        SharedData.joel_camilo_cell_scene.add_object(GameObject("roof_l", Vec2(0, 0), Vec2(40, 2), Textured("texture/floor") ))
        SharedData.joel_camilo_cell_scene.add_object(GameObject("roof_r", Vec2(60, 0), Vec2(40, 2), Textured("texture/floor") ))
        SharedData.joel_camilo_cell_scene.add_object(
            GameObject(
                "gate_hallway_joel", Vec2(40, 0), Vec2(20, 2),
                Textured("texture/gate"),
                SceneSwapper(SharedData.hallway_scene, "go to hallway","player", Vec2(140, 30))
            )
        )

        #couryard scene
        SharedData.courtyard_scene.add_object(
            GameObject(
                "hallway_gate", Vec2(0, 10), Vec2(2, 20),
                Textured("texture/gate"),
                SceneSwapper(SharedData.hallway_scene, "go to  hallway","player", Vec2(190, 25))
            )
        )
        SharedData.courtyard_scene.add_object(GameObject("left_wall_up", Vec2(0, 0), Vec2(2, 10), Textured("texture/wall")))
        SharedData.courtyard_scene.add_object(GameObject("left_wall_down", Vec2(0, 30), Vec2(2, 10), Textured("texture/wall")))
        SharedData.courtyard_scene.add_object(GameObject("roof2", Vec2(0, 0), Vec2(100, 2), Textured("texture/floor")))
        SharedData.courtyard_scene.add_object(GameObject("right_wall", Vec2(98, 0), Vec2(2, 40), Textured("texture/wall")))
        SharedData.courtyard_scene.add_object(GameObject("roof3", Vec2(0, 38), Vec2(100, 2), Textured("texture/floor")))


        #second hallway
        SharedData.hallway_second_scene.add_object(GameObject("right_wall_up", Vec2(198, 0), Vec2(2, 10), Textured("texture/wall")))
        SharedData.hallway_second_scene.add_object(GameObject("right_wall_down", Vec2(198, 30), Vec2(2, 10), Textured("texture/wall")))
        SharedData.hallway_second_scene.add_object(
            GameObject(
                "hallway_gate", Vec2(198, 10), Vec2(2, 20),
                Textured("texture/gate"),
                SceneSwapper(SharedData.hallway_scene, "go to hallway","player", Vec2(20, 25))
            )
        )
        SharedData.hallway_second_scene.add_object(GameObject("left_wall", Vec2(0, 0), Vec2(2, 40), Textured("texture/wall")))
        SharedData.hallway_second_scene.add_object(GameObject("floor_l9", Vec2(0, 0), Vec2(90, 2), Textured("texture/floor")))
        SharedData.hallway_second_scene.add_object(GameObject("floor_r9", Vec2(0, 0), Vec2(200, 2), Textured("texture/floor")))
        SharedData.hallway_second_scene.add_object(GameObject("floor_m9", Vec2(0, 0), Vec2(200, 2), Textured("texture/floor")))
        SharedData.hallway_second_scene.add_object(GameObject("roof_r6", Vec2(180, 38), Vec2(20, 2), Textured("texture/floor")))
        SharedData.hallway_second_scene.add_object(GameObject("roof_l6", Vec2(0, 38), Vec2(140, 2), Textured("texture/floor")))
        SharedData.hallway_second_scene.add_object(
            GameObject(
                "cafeteria_gate", Vec2(140, 38), Vec2(40, 2),
                Textured("texture/gate"),
                SceneSwapper(SharedData.cafeteria_scene, "go to cafeteria","player", Vec2(25, 25))
            )
        )


        #cafeteria
        SharedData.cafeteria_scene.add_object(GameObject("left_wall", Vec2(0, 0), Vec2(2, 80), Textured("texture/wall")))
        SharedData.cafeteria_scene.add_object(GameObject("right_wall", Vec2(58, 0), Vec2(2, 80), Textured("texture/wall")))
        SharedData.cafeteria_scene.add_object(GameObject("roof10", Vec2(0, 78), Vec2(60, 2), Textured("texture/floor")))
        SharedData.cafeteria_scene.add_object(GameObject("floor_r10", Vec2(50, 0), Vec2(10, 2), Textured("texture/floor")))
        SharedData.cafeteria_scene.add_object(GameObject("floor_l10", Vec2(0, 0), Vec2(10, 2), Textured("texture/floor")))
        SharedData.cafeteria_scene.add_object(
            GameObject(
                "cafeteria_hallway_gate", Vec2(10, 0), Vec2(40, 2),
                Textured("texture/gate"),
                SceneSwapper(SharedData.hallway_second_scene, "go to second hallway","player", Vec2(160, 30))
            )
        )

        buffer.set_scene(SharedData.player_cell_scene)

    def pre_frame(self, buffer: SceneKonsoleBuffer):
        pass

def register_loader():
    PrisonGameLoader().register_self()

#PlaySound('res/sounds/testmusic1.wav', 0)

