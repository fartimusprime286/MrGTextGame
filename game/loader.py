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
        #create hallway scene - set_large enable pseudo-camera tracking
        SharedData.hallway_scene = buffer.create_scene().set_large()
        SharedData.bill_cell_scene = buffer.create_scene()

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

        SharedData.player_cell_scene.add_object(GameObject("player", Vec2(10, 10), Vec2(4, 4), PlayerBehavior(), RigidBody()))
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
        SharedData.hallway_scene.add_object(GameObject("roof_r", Vec2(60, 0), Vec2(100, 2), Textured("texture/floor")))

        #SharedData.hallway_scene.add_object(GameObject("left_wall", Vec2(0, 0), Vec2(2, 40), Textured("texture/wall")))
        #SharedData.hallway_scene.add_object(GameObject("right_wall", Vec2(98, 0), Vec2(2, 40), Textured("texture/wall")))

        #floor
        SharedData.hallway_scene.add_object(GameObject("floor_l", Vec2(0, 38), Vec2(40, 2), Textured("texture/floor")))
        SharedData.hallway_scene.add_object(
            GameObject(
                "gate_bill", Vec2(40, 38), Vec2(20, 2),
                Textured("texture/gate"),
                SceneSwapper(SharedData.bill_cell_scene, "go to bills cell", "player", Vec2(40, 10))
            )
        )
        SharedData.hallway_scene.add_object(GameObject("floor_r", Vec2(60, 38), Vec2(100, 2), Textured("texture/floor")))

        buffer.set_scene(SharedData.player_cell_scene)

    def pre_frame(self, buffer: SceneKonsoleBuffer):
        pass

def register_loader():
    PrisonGameLoader().register_self()