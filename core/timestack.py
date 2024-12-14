import time
from collections.abc import Callable


class TimeStack:
    def __init__(self):
        self._children: dict[str, TimeStack] = {}
        self.actions: dict[str, float] = {}

    def get_or_create_category(self, name: str):
        exising = self._children.get(name)
        if exising is not None:
            return exising

        category = TimeStack()
        self._children[name] = category
        return category

    def time_action(self, name: str, action: Callable[[], None]):
        start_time = time.perf_counter_ns()
        action()
        end_time = time.perf_counter_ns()
        self.actions[name] = (end_time - start_time)
        return self

    def reset(self):
        self._children = {}
        self.actions = {}

    def get_elapsed_time(self) -> int:
        total_elapsed_time = 0
        for category in self._children.values():
            total_elapsed_time += category.get_elapsed_time()

        for action_time in self.actions.values():
            total_elapsed_time += action_time

        return total_elapsed_time

    def pretty_str(self, override_name: (str | None) = None) -> str:
        name = "TimeStack"
        if override_name is not None:
            name = override_name

        pretty_str = f"{name}:\n"
        for (name, category) in self._children.items():
            cat_p_str: str = category.pretty_str(name)
            lines = cat_p_str.splitlines()
            for i in range(len(lines)):
                pretty_str += "  " + lines[i] + "\n"

        for (action, action_time) in self.actions.items():
            pretty_str += f"  {action}: {action_time}ns {action_time / 1000000}ms\n"

        elapsed_time = self.get_elapsed_time()
        pretty_str += f"  Elapsed time: {elapsed_time}ns {elapsed_time / 1000000}ms\n"

        return pretty_str

    def __str__(self) -> str:
        return self.pretty_str()
