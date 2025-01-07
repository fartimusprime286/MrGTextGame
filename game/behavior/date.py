from core import DateRange
from core.behavior import Interactable
from core.game import ObjectBehavior, Collider
from core.konsole import KonsoleBuffer
from data import SharedData


class DatedBehavior(Interactable):
    def __init__(self, behavior: ObjectBehavior, date_range: DateRange):
        super().__init__()
        self.behavior = behavior
        self.date_range = date_range
        self._has_loaded = False

    def on_load(self, buffer: KonsoleBuffer):
        self.behavior._parent = self._parent

        if self.date_range.accepts(SharedData.current_date):
            self.behavior.on_load(buffer)
            self._has_loaded = True

    def update(self, buffer: KonsoleBuffer):
        self.behavior._parent = self._parent

        if not self.date_range.accepts(SharedData.current_date):
            self._parent.is_raycast_collidable = False
            return

        self._parent.is_raycast_collidable = True

        if not self._has_loaded:
            self.behavior.on_load(buffer)
            self._has_loaded = True

        self.behavior.update(buffer)

    def render(self, buffer: KonsoleBuffer):
        self.behavior._parent = self._parent

        if not self.date_range.accepts(SharedData.current_date):
            return

        self.behavior.render(buffer)

    def while_colliding(self, other: Collider):
        self.behavior._parent = self._parent

        if not self.date_range.accepts(SharedData.current_date):
            return

        self.behavior.while_colliding(other)

    def interaction_name(self) -> str:
        if isinstance(self.behavior,Interactable):
            return self.behavior.interaction_name()
        return ""

    def on_interact(self, buffer: KonsoleBuffer, interaction_data):
        if isinstance(self.behavior,Interactable):
            return self.behavior.on_interact(buffer,interaction_data)
