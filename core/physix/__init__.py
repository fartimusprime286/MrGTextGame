from typing import cast

from core import Vec2
from core.game import ObjectBehavior, Collider, GameObject
from core.konsole import KonsoleBuffer


class RigidBody(ObjectBehavior):
    def __init__(self, raycast_accuracy: float = 0.25, raycast_max_travel: float = 0.5):
        super().__init__()
        self.velocity = Vec2(0, 0)
        self.raycast_accuracy = raycast_accuracy
        self.raycast_max_travel = raycast_max_travel

    def on_load(self, buffer: KonsoleBuffer):
        pass

    def update(self, buffer: KonsoleBuffer):
        parent: GameObject = cast(GameObject, self._parent)
        raycast_left = parent.scene.raycast(parent.pos + Vec2(0, 1), Vec2(self.raycast_accuracy, 0), Vec2(1, parent.size.y - 2), self.raycast_max_travel, lambda game_obj: game_obj is not parent)
        raycast_right = parent.scene.raycast(parent.pos + Vec2(parent.size.x - 1, 1), Vec2(-self.raycast_accuracy, 0), Vec2(1, parent.size.y - 2), self.raycast_max_travel, lambda game_obj: game_obj is not parent)
        raycast_up = parent.scene.raycast(parent.pos + Vec2(1, 0), Vec2(0, -self.raycast_accuracy), Vec2(parent.size.x - 2, 1), self.raycast_max_travel, lambda game_obj: game_obj is not parent)
        raycast_down = parent.scene.raycast(parent.pos + Vec2(1, parent.size.y - 1), Vec2(0,  self.raycast_accuracy), Vec2(parent.size.x - 2, 1), self.raycast_max_travel, lambda game_obj: game_obj is not parent)

        collided_left = raycast_left[0] is not None
        collided_right = raycast_right[0] is not None
        collided_up = raycast_up[0] is not None
        collided_down = raycast_down[0] is not None

        if collided_left:
            self.velocity.x = max(self.velocity.x, 0)
        if collided_right:
            self.velocity.x = min(self.velocity.x, 0)
        if collided_up:
            self.velocity.y = max(self.velocity.y, 0)
        if collided_down:
            self.velocity.y = min(self.velocity.y, 0)

        parent.pos += self.velocity

    def render(self, buffer: KonsoleBuffer):
        pass

    def while_colliding(self, other: Collider):
        pass