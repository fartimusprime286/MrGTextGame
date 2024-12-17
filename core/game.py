import threading
from abc import abstractmethod, ABC
from typing import Self, Callable

from core import Vec2, BoundingBox
from core.konsole import KonsoleBuffer


class Collider:
    def __init__(self, name: str, pos: Vec2, size: Vec2):
        self.name = name
        self.pos = pos
        self.size = size

    def bounding_box(self) -> BoundingBox:
        return BoundingBox(self.pos, self.pos + self.size)

    def is_colliding_with(self, other) -> bool:
        return self.bounding_box().is_overlapping(other.bounding_box())

class ObjectBehavior(ABC):
    def __init__(self):
        self._parent: (Collider | None) = None

    def set_parent(self, parent: Collider):
        current_parent: (GameObject | Collider) = self._parent
        new_parent: (GameObject | Collider) = parent
        if isinstance(current_parent, GameObject) and isinstance(new_parent, GameObject):
            current_parent.remove_behavior(self)
            new_parent.add_behavior(self)

    @abstractmethod
    def on_load(self, buffer: KonsoleBuffer):
        pass

    @abstractmethod
    def update(self, buffer: KonsoleBuffer):
        pass

    @abstractmethod
    def render(self, buffer: KonsoleBuffer):
        pass

    @abstractmethod
    def while_colliding(self, other: Collider):
        pass


class GameObject(Collider):
    def __init__(self, name: str, pos: Vec2, size: Vec2, *default_behaviors: ObjectBehavior):
        super().__init__(name, pos, size)

        self.behaviors: list[ObjectBehavior] = []
        for behavior in default_behaviors:
            self.add_behavior(behavior)

        self.scene = None

    def add_behavior(self, behavior: ObjectBehavior):
        behavior._parent = self
        self.behaviors.append(behavior)

    def has_behavior_of_type[T](self, behavior_type: type[T]) -> bool:
        behaviors_of_type = self.get_behavior_by_type(behavior_type)
        return bool(behaviors_of_type)

    def get_behavior_by_type[T](self, behaviour_type: type[T]) -> list[T]:
        matching: list[T] = []
        for behavior in self.behaviors:
            if isinstance(behavior, behaviour_type):
                matching.append(behavior)

        return matching

    def remove_behavior(self, behavior: ObjectBehavior):
        self.behaviors.remove(behavior)
        behavior._parent = None

    def load(self, buffer: KonsoleBuffer):
        for behavior in self.behaviors:
            behavior.on_load(buffer)

    def update(self, buffer: KonsoleBuffer):
        for behavior in self.behaviors:
            behavior.update(buffer)

    def render(self, buffer: KonsoleBuffer):
        for behavior in self.behaviors:
            behavior.render(buffer)

    def while_colliding(self, other: Self):
        for behavior in self.behaviors:
            behavior.while_colliding(other)

class Scene:
    def __init__(self, buffer: KonsoleBuffer):
        self._thread_lock = threading.Lock()
        self._objects: dict[str, GameObject] = dict()
        self.buffer: KonsoleBuffer = buffer
        self._deletion_buffer: list[str] = []
        self._addition_buffer: list[GameObject] = []
        self._large = False

    def set_large(self) -> Self:
        self._large = True
        return self

    def is_large(self) -> bool:
        return self._large

    def add_object(self, game_object: GameObject):
        self._addition_buffer.append(game_object)

    def get_object(self, obj_id: str) -> (GameObject | None):
        return self._objects.get(obj_id, None)

    def _add_object(self, game_object: GameObject):
        self._objects[game_object.name] = game_object
        game_object.load(self.buffer)
        game_object.scene = self

    def remove_object(self, obj_id: str) -> (GameObject | None):
        self._deletion_buffer.append(obj_id)
        return self._objects.get(obj_id, None)

    def raycast(self, start_pos: Vec2, direction: Vec2, collider_size: Vec2 = Vec2(0, 0), max_travel: float = 10000, selector: Callable[[GameObject], bool] = lambda obj: True) -> tuple[(GameObject | None), Vec2, float]:
        if direction.magnitude() == 0:
            return None, Vec2(0, 0), 0
        pos = start_pos

        while pos.distance_to(start_pos) < max_travel:
            collider = Collider("raycast_collider", pos, collider_size)
            for game_object in self._objects.values():
                if collider.bounding_box().is_overlapping(game_object.bounding_box()):
                    if selector(game_object):
                        return game_object, (pos - start_pos), pos.distance_to(start_pos)
            pos += direction

        return None, pos - start_pos, pos.distance_to(start_pos)

    def process_object_changes(self):
        with self._thread_lock:
            for game_object in self._addition_buffer:
                self._add_object(game_object)

            for name in self._deletion_buffer:
                self._objects.pop(name, None)

            self._addition_buffer = []
            self._deletion_buffer = []

    def update(self):
        with self._thread_lock:
            for obj in self._objects.values():
                obj.update(self.buffer)
                for obj2 in self._objects.values():
                    if obj.is_colliding_with(obj2):
                        obj.while_colliding(obj2)

    def render(self):
        with self._thread_lock:
            for obj in self._objects.values():
                obj.render(self.buffer)

    def objects(self):
        return self._objects

class SceneKonsoleBuffer(KonsoleBuffer):
    def __init__(self, dimensions: Vec2):
        super().__init__(dimensions)
        self._scene: Scene = Scene(self)
        self._new_scene: (Scene | None) = None
        self._should_quit = False

    def create_scene(self) -> Scene:
        return Scene(self)

    def set_scene(self, scene: Scene):
        self._new_scene = scene

    def update(self):
        self._scene.update()
        self._scene.process_object_changes()
        if self._new_scene is not None:
            self._scene = self._new_scene
            self._new_scene = None

    def quit(self):
        self._should_quit = True

    def should_quit(self):
        return self._should_quit

    def scene(self):
        return self._scene

    def flush(self):
        self._scene.render()
        super().flush()

class GameLoader:
    loaders = []

    def register_self(self):
        GameLoader.loaders.append(self)
        return self

    @staticmethod
    def register_loader(loader):
        GameLoader.loaders.append(loader)

    @staticmethod
    def invoke_on_make_buffer(buffer: SceneKonsoleBuffer):
        for loader in GameLoader.loaders:
            loader.on_make_buffer(buffer)

    @staticmethod
    def invoke_pre_frame(buffer: SceneKonsoleBuffer):
        for loader in GameLoader.loaders:
            loader.pre_frame(buffer)

    @abstractmethod
    def on_make_buffer(self, buffer: SceneKonsoleBuffer):
        pass

    @abstractmethod
    def pre_frame(self, buffer: SceneKonsoleBuffer):
        pass
