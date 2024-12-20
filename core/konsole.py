import logging
import os
import time
from typing import Callable

import core.logging
from core import Vec2, Color, DefaultColors
from core.texture import TextureLoader


def clear_console():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

class KonsoleBuffer:
    def __init__(self, dimensions: Vec2):
        self.dimensions: Vec2 = dimensions
        self._buffer: list[list[str]] = []
        self._frame_tracker = FrameTracker()
        self.offset = Vec2(0, 0)
        self.max_offsetted_dimensions = Vec2(self.dimensions.x / 2, self.dimensions.y)
        self._draw_fps = False
        self._cap_fps = True
        self.clear_buffer()

    def set_fps_target(self, target: float):
        self._frame_tracker.target_fps = target

    def set_draw_fps(self, draw_fps: bool):
        self._draw_fps = draw_fps

    def enable_fps_cap(self):
        self._cap_fps = True

    def disable_fps_cap(self):
        self._cap_fps = False

    def flush(self):
        rendered_string = ""

        for row in self._buffer:
            for char in row:
                rendered_string += char
            rendered_string += "\n"

        clear_console()
        if self._draw_fps: print("average fps = " + str(int(self._frame_tracker.average_fps())) + "\n\n\n")
        print(rendered_string)

        self.clear_buffer()
        if self._cap_fps: self._frame_tracker.wait_until_target()
        self._frame_tracker.log_frame(time.time())

    def pixel_at(self, pos: Vec2) -> str:
        return self._buffer[int(pos.y)][int(pos.x)]

    def _is_out_of_bounds(self, pos: Vec2, dimensions: Vec2) -> bool:
        return pos.x >= dimensions.x or pos.x < 0 or pos.y >= dimensions.y or pos.y < 0

    def is_out_of_bounds(self, pos: Vec2) -> bool:
        return self._is_out_of_bounds(pos, self.dimensions)

    def draw_char_no_color(self, pos: Vec2, char: str, draw_offsetted: bool = True):
        if draw_offsetted:
            n_pos = pos + self.offset
            is_oob = self._is_out_of_bounds(n_pos, self.dimensions)
            #core.logging.debug(f"Pos: {pos}, offset pos: {n_pos}, oob: {is_oob}, x: {n_pos.x >= self.max_offsetted_dimensions.x or pos.x < 0}, y: {n_pos.y >= self.max_offsetted_dimensions.y or pos.y < 0}")
            if self._is_out_of_bounds(n_pos, self.max_offsetted_dimensions): return
        else:
            n_pos = pos
            if self.is_out_of_bounds(n_pos): return

        self._buffer[int(n_pos.y)][int(n_pos.x)] = char

    def draw_char(self, pos: Vec2, char: str, draw_offsetted: bool = True, color: Color = DefaultColors.NONE.value, background_color: Color = DefaultColors.NONE.value):
        self.draw_char_no_color(pos, color.with_background_color(background_color) + char + Color.reset_string(), draw_offsetted)

    def draw_text(self, pos: Vec2, text: str, wrap=False, max_chars_in_row: (int | None) = None, begin_x0_nl=True, draw_offsetted: bool = True, color_mapper: Callable[[Vec2], Color] = lambda v: DefaultColors.NONE.value, bg_color_mapper: Callable[[Vec2], Color] = lambda v: DefaultColors.NONE.value):
        content: list[str] = [text]
        if wrap:
            per_line = self.dimensions.x - pos.x
            if max_chars_in_row is not None:
                per_line = max_chars_in_row

            content = [text[i:i+per_line] for i in range(0, len(text), per_line)]

        for y_offset in range(len(content)):
            if pos.y + y_offset >= self.dimensions.y: continue
            line = content[y_offset]
            for x_offset in range(len(line)):
                new_pos = pos
                if y_offset > 0 & begin_x0_nl:
                    new_pos = Vec2(0, pos.y)

                if new_pos.x + x_offset >= self.dimensions.x: continue
                char = line[x_offset]

                new_pos += Vec2(x_offset, y_offset)

                self.draw_char(new_pos, char, draw_offsetted, color_mapper(new_pos), bg_color_mapper(new_pos))

    def draw_texture(self, pos: Vec2, size: (Vec2 | None), texture_id: str, draw_offsetted: bool = True):
        texture = TextureLoader.textures[texture_id]
        if size is None:
            size = Vec2(texture.width, texture.height)

        texture_data = texture.resized(size)
        content = texture_data[0]
        colors = texture_data[1]
        for y_offset in range(len(content)):
            line = content[y_offset]
            for x_offset in range(len(line)):
                char = line[x_offset]
                offset = Vec2(x_offset, y_offset)
                color = colors[offset]
                new_pos = pos + offset

                if color == DefaultColors.NONE.value:
                    continue

                #core.logging.debug(f"char at: {offset}, {color.mode_reliant(texture.color_mode) + char + Color.reset_string()}")

                self.draw_char_no_color(new_pos, color.mode_reliant(texture.color_mode) + char + Color.reset_string(), draw_offsetted)

    def draw_rect(self, pos: Vec2, size: Vec2, draw_offsetted: bool = True, color: Color = DefaultColors.NONE.value):
        char = color.to_background_color() + " " + Color.reset_string()

        for x in range(int(size.x)):
            for y in range(int(size.y)):
                c_pos = pos + Vec2(x, y)
                self.draw_char_no_color(c_pos, char, draw_offsetted)

    def clear_buffer(self):
        self._buffer = []
        while len(self._buffer) < self.dimensions.y:
            self._buffer.append(list(" " * int(self.dimensions.x)))

class FrameTracker:
    def __init__(self):
        self.init_time = time.time()
        self.target_fps = 12.2
        self._frame_logs: list[list[float]] = []

    def log_frame(self, end_time):
        last_frame_log = self._last_frame_log(fallback = end_time)

        actual_time = last_frame_log[1]
        frame_time = end_time - actual_time

        self._frame_logs.append([frame_time, end_time])
        self._trim_to_size()

    def average_fps(self) -> float:
        if len(self._frame_logs) <= 0: return 0.0

        total_frame_time = 0
        for frame_log in self._frame_logs:
            total_frame_time += frame_log[0]

        average_frame_time = total_frame_time / len(self._frame_logs)

        if average_frame_time == 0: return 0.0

        return 1 / average_frame_time

    def wait_until_target(self):
        frequency = 1 / self.target_fps
        last_frame_log = self._last_frame_log(time.time())
        sleep_time = frequency - (time.time() - last_frame_log[1])
        if sleep_time >= 0: time.sleep(sleep_time)

    def _last_frame_log(self, fallback) -> list[float]:
        last_frame_log = [fallback, fallback]
        if len(self._frame_logs) > 0:
            last_frame_log = self._frame_logs[-1]

        return last_frame_log

    def _trim_to_size(self):
        if len(self._frame_logs) > 5 * self.target_fps:
            to_remove = int(len(self._frame_logs) - (5 * self.target_fps))
            self._frame_logs = self._frame_logs[to_remove:]
