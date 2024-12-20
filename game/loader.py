from core import Vec2
from core.behavior import Textured
from core.text import TextRoot
from game.behavior.bed import BedBehavior
from game.behavior.character import Gretchen, GretchenProxyBehavior, Geff
from game.behavior.character.warden import Warden
from game.behavior.collectibles import Collectible
from game.behavior.officer import OfficeGate
from game.behavior.scene import SceneSwapper
from core.physix import RigidBody
from game.behavior.player import PlayerBehavior
from core.game import GameLoader, SceneKonsoleBuffer, GameObject
from data import SharedData
from game.behavior.showers import ShowersGate, Vent
from game.behavior import ExamplePersonBehavior, TextBoxBehavior
from game.behavior import RouletteBehavior


class PrisonGameLoader(GameLoader):
    def on_make_buffer(self, buffer: SceneKonsoleBuffer):


        #tutorial scene
        SharedData.casino_scene = buffer.create_scene().set_large()
        #create player cell
        SharedData.player_cell_scene = buffer.create_scene()
        #create hallway scene - set_large enable pseudo-camera tracking
        SharedData.hallway_scene = buffer.create_scene().set_large()
        SharedData.hallway_second_scene = buffer.create_scene().set_large()
        SharedData.cafeteria_scene = buffer.create_scene().set_large()
        SharedData.bill_cell_scene = buffer.create_scene()
        SharedData.joel_camilo_cell_scene = buffer.create_scene()
        SharedData.lucas_julien_cerrato_cell_scene = buffer.create_scene()
        SharedData.courtyard_scene = buffer.create_scene()
        SharedData.showers_scene = buffer.create_scene()
        SharedData.office_scene = buffer.create_scene()
        SharedData.outside_scene = buffer.create_scene()
        SharedData.vent_scene = buffer.create_scene().set_large()


        #tutorial data
        SharedData.casino_scene.add_object(GameObject("roof", Vec2(0, 0), Vec2(200, 2), Textured("texture/floor")))
        SharedData.casino_scene.add_object(GameObject("floor", Vec2(0, 51), Vec2(200, 2), Textured("texture/floor")))
        SharedData.casino_scene.add_object(GameObject("left_wall", Vec2(0, 0), Vec2(2, 53), Textured("texture/wall")))
        SharedData.casino_scene.add_object(GameObject("right_wall_up", Vec2(198, 0), Vec2(2, 17.5), Textured("texture/wall")))
        SharedData.casino_scene.add_object(GameObject("right_wall_down", Vec2(198, 37.5), Vec2(2, 15.5), Textured("texture/wall")))
        SharedData.casino_scene.add_object(GameObject("casino_closed_gate", Vec2(198, 17.5), Vec2(2, 20), Textured("texture/gate")))
        SharedData.casino_scene.add_object(GameObject("wall_stair", Vec2(80, 22.5), Vec2(40, 2), Textured("texture/wall")))
        SharedData.casino_scene.add_object(GameObject("wall_stair2", Vec2(80, 30.5), Vec2(40, 2), Textured("texture/wall")))
        SharedData.casino_scene.add_object(GameObject("wall_stair3", Vec2(118, 22.5), Vec2(2, 10), Textured("texture/wall")))
        SharedData.casino_scene.add_object(GameObject("roulette_table1", Vec2(8, 5), Vec2(32, 16), Textured("texture/roulette_table"),RouletteBehavior()))
        SharedData.casino_scene.add_object(GameObject("roulette_table2", Vec2(8, 32), Vec2(32, 16), Textured("texture/roulette_table"),RouletteBehavior()))



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

        SharedData.player_cell_scene.add_object(GameObject("player", Vec2(10, 10), Vec2(10, 10), PlayerBehavior(), RigidBody()))
        #testing teleport
        '''SharedData.player_cell_scene.add_object(
            GameObject(
                "portal", Vec2(40, 28), Vec2(10, 2),
                Textured("texture/gate"),
                SceneSwapper(SharedData.casino_scene, "go gambling", "player", Vec2(40, 10))
            )
        )
        '''
        #summon player
        SharedData.casino_scene.add_object(GameObject("player", Vec2(190, 25), Vec2(10, 10), PlayerBehavior(), RigidBody()))
        begfeedback = TextRoot("Let's go gambling! how about some roulette \n Use wasd to move around and backslash to interact \n Press enter to continue")
        SharedData.casino_scene.add_object(GameObject("tbox", Vec2(10, 10), Vec2(90, 30),TextBoxBehavior(begfeedback)))

        SharedData.player_cell_scene.add_object(GameObject("bed", Vec2(86, 3), Vec2(10, 10), Textured("texture/bed"), BedBehavior()))
        SharedData.player_cell_scene.add_object(GameObject("ball_person", Vec2(15, 30), Vec2(4, 4),Textured("texture/ball"),ExamplePersonBehavior()))

        #Warden
        SharedData.outside_scene.add_object(GameObject("warden", Vec2(15, 20), Vec2(9, 10),Warden()))

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
        SharedData.lucas_julien_cerrato_cell_scene.add_object(GameObject("floor4_l", Vec2(0, 38), Vec2(40, 2), Textured("texture/floor")))
        SharedData.lucas_julien_cerrato_cell_scene.add_object(
            GameObject(
                "gate_hallway_lucas", Vec2(40, 38), Vec2(20, 2),
                Textured("texture/gate"),
                SceneSwapper(SharedData.hallway_scene, "go to hallway", "player", Vec2(140, 10))
            )
        )
        SharedData.lucas_julien_cerrato_cell_scene.add_object(GameObject("floor4_r", Vec2(60, 38), Vec2(40, 2), Textured("texture/floor")))

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
        SharedData.courtyard_scene.add_object(GameObject("geff", Vec2(85, 25), Vec2(10, 10), Geff()))


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
        SharedData.hallway_second_scene.add_object(GameObject("floor_r9", Vec2(170, 0), Vec2(30, 2), Textured("texture/floor")))
        SharedData.hallway_second_scene.add_object(GameObject("floor_m9", Vec2(110, 0), Vec2(40, 2), Textured("texture/floor")))
        SharedData.hallway_second_scene.add_object(GameObject("roof_r6", Vec2(180, 38), Vec2(20, 2), Textured("texture/floor")))
        SharedData.hallway_second_scene.add_object(GameObject("roof_l6", Vec2(0, 38), Vec2(140, 2), Textured("texture/floor")))
        SharedData.hallway_second_scene.add_object(
            GameObject(
                "cafeteria_gate", Vec2(140, 38), Vec2(40, 2),
                Textured("texture/gate"),
                SceneSwapper(SharedData.cafeteria_scene, "go to cafeteria","player", Vec2(45, 4))
            )
        )
        SharedData.hallway_second_scene.add_object(
            GameObject(
                "showers_gate", Vec2(150, 0), Vec2(20, 2),
                Textured("texture/gate"),
                ShowersGate(SharedData.showers_scene, "go to showers","player", Vec2(20, 25))
            )
        )
        SharedData.hallway_second_scene.add_object(
            GameObject(
                "office_gate", Vec2(90, 0), Vec2(20, 2),
                Textured("texture/gate"),
                OfficeGate(SharedData.office_scene, "go to office", "player", Vec2(80, 30))
            )
        )

        #cafeteria
        SharedData.cafeteria_scene.add_object(GameObject("left_wall", Vec2(0, 0), Vec2(2, 70), Textured("texture/wall")))
        SharedData.cafeteria_scene.add_object(GameObject("right_wall", Vec2(98, 0), Vec2(2, 70), Textured("texture/wall")))
        SharedData.cafeteria_scene.add_object(GameObject("roof10", Vec2(0, 68), Vec2(2, 2), Textured("texture/floor")))
        SharedData.cafeteria_scene.add_object(GameObject("floor_r10", Vec2(70, 0), Vec2(30, 2), Textured("texture/floor")))
        SharedData.cafeteria_scene.add_object(GameObject("floor_l10", Vec2(0, 0), Vec2(30, 2), Textured("texture/floor")))
        SharedData.cafeteria_scene.add_object(
            GameObject(
                "cafeteria_hallway_gate", Vec2(30, 0), Vec2(40, 2),
                Textured("texture/gate"),
                SceneSwapper(SharedData.hallway_second_scene, "go to second hallway","player", Vec2(160, 26))
            )
        )

        SharedData.cafeteria_scene.add_object(GameObject("gretchen", Vec2(44, 50), Vec2(10, 10), Gretchen()))
        SharedData.cafeteria_scene.add_object(GameObject("gretchens_table", Vec2(34, 46), Vec2(30, 3), Textured("texture/table"), GretchenProxyBehavior()))

        #office
        SharedData.office_scene.add_object(GameObject("roof", Vec2(0, 0), Vec2(100, 2), Textured("texture/floor")))
        SharedData.office_scene.add_object(GameObject("left_wall", Vec2(0, 0), Vec2(2, 40), Textured("texture/wall")))
        SharedData.office_scene.add_object(GameObject("right_wall", Vec2(98, 0), Vec2(2, 40), Textured("texture/wall")))
        SharedData.office_scene.add_object(GameObject("floor4_l", Vec2(0, 38), Vec2(60, 2), Textured("texture/floor")))
        SharedData.office_scene.add_object(GameObject("floor4_r", Vec2(80, 38), Vec2(20, 2), Textured("texture/floor")))
        SharedData.office_scene.add_object(
            GameObject(
            "gate_hallway_office", Vec2(60, 38), Vec2(20, 2),
            Textured("texture/gate"),
            SceneSwapper(SharedData.hallway_second_scene, "go to second hallway", "player", Vec2(100, 15))
            )
        )

        SharedData.office_scene.add_object(GameObject("key_collectible", Vec2(80, 10), Vec2(10, 5), Collectible("key")))

        #showers
        SharedData.showers_scene.add_object(GameObject("roof", Vec2(0, 0), Vec2(100, 2), Textured("texture/floor")))
        SharedData.showers_scene.add_object(GameObject("left_wall", Vec2(0, 0), Vec2(2, 40), Textured("texture/wall")))
        SharedData.showers_scene.add_object(GameObject("right_wall", Vec2(98, 0), Vec2(2, 40), Textured("texture/wall")))
        SharedData.showers_scene.add_object(GameObject("floor4_l", Vec2(0, 38), Vec2(20, 2), Textured("texture/floor")))
        SharedData.showers_scene.add_object(GameObject("floor4_r", Vec2(40, 38), Vec2(60, 2), Textured("texture/floor")))
        SharedData.showers_scene.add_object(
            GameObject(
                "gate_hallway_showers", Vec2(20, 38), Vec2(20, 2),
                Textured("texture/gate"),
                SceneSwapper(SharedData.hallway_second_scene, "go to second hallway", "player", Vec2(160, 15))
            )
        )

        #shower vent
        SharedData.showers_scene.add_object(GameObject(
            "vent",
            Vec2(4, 2),
            Vec2(16, 8),
            Textured("texture/vent"),
            Vent(SharedData.vent_scene, "enter vent", "player", Vec2(82, 2))
        ))

        #vent scene
        SharedData.vent_scene.add_object(GameObject("roof",       Vec2(0, 0),   Vec2(100, 2), Textured("texture/floor")))
        SharedData.vent_scene.add_object(GameObject("floor",      Vec2(0, 14),  Vec2(100, 2), Textured("texture/floor")))
        SharedData.vent_scene.add_object(GameObject(
            "left_wall",
            Vec2(0, 2),
            Vec2(2, 12),
            Textured("texture/gate"),
            SceneSwapper(SharedData.office_scene, "exit vents (office)", "player", Vec2(10, 10))
        ))

        SharedData.vent_scene.add_object(GameObject(
            "right_wall",
            Vec2(98, 2),
            Vec2(2, 12),
            Textured("texture/gate"),
            SceneSwapper(SharedData.showers_scene, "exit vents (showers)", "player", Vec2(22, 4))
        ))

        buffer.set_scene(SharedData.casino_scene)

    def pre_frame(self, buffer: SceneKonsoleBuffer):
        pass

def register_loader():
    PrisonGameLoader().register_self()

#PlaySound('res/sounds/testmusic1.wav', 0)

