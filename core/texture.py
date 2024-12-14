import json
import os
import re

from PIL import Image
from PIL.Image import Resampling

from core import Color, Vec2, NONE_COLOR


"""
JSON Model

{
    "texture_location": "res/texture.png",
    //can be either "foreground" or "background"
    "color_mode": "foreground",
    //optional
    "rescale": [width, height]
    //default: " "
    "default_char": "x"
    "color_to_char": {
        "rgb(255, 255, 255)": "X"
    }
}

"""

class Texture:
    RGB_REGEX = re.compile(r"rgb\( *(\d*), *(\d*), *(\d*) *\)")

    def __init__(self, texture_location):
        with open(texture_location, "r") as char_data:
            json_data = json.load(char_data)
            self.texture_location = json_data["texture_location"]
            self.color_mode = json_data["color_mode"]
            rescale = json_data.get("rescale")
            self._validate_color_mode()
            self.default_char = json_data.get("default_char", " ")

            color_to_char_dict = json_data["color_to_char"]
            color_to_char: dict[Color, str] = dict()

            for color in color_to_char_dict.keys():
                match = Texture.RGB_REGEX.fullmatch(color)
                if not match: raise Exception(f"Invalid regex found in texture file {texture_location}, regex: {color}")
                r = int(match.group(1))
                g = int(match.group(2))
                b = int(match.group(3))
                true_color = Color(r, g, b)

                char = color_to_char_dict[color]
                color_to_char[true_color] = char

            self.color_to_char = color_to_char

        image = Image.open(self.texture_location)
        self._resize_cache: dict[Vec2, tuple[list[str], dict[Vec2, Color]]] = dict()

        if rescale is not None:
            image = image.resize(rescale, Resampling.LANCZOS)

        char_data, color_data = self._compute_data(image)

        self._resize_cache[Vec2(image.width, image.height)] = (char_data, color_data)
        self.width = image.width
        self.height = image.height

        self.char_data = char_data
        self.color_data = color_data

        image.close()

    def resized(self, size: Vec2) -> tuple[list[str], dict[Vec2, Color]]:
        image = Image.open(self.texture_location)

        data = self._resize_cache.get(size)
        if data is None:
            image = image.resize((int(size.x), int(size.y)), Resampling.LANCZOS)
            data = self._compute_data(image)
            self._resize_cache[size] = data

        image.close()
        return data

    def _compute_data(self, image: Image) -> tuple[list[str], dict[Vec2, Color]]:
        char_data: list[str] = list()
        color_data: dict[Vec2, Color] = dict()

        for y in range(image.height):
            row = ""
            for x in range(image.width):
                pixel = image.getpixel((x, y))
                #some PNGs don't contain transparency data
                try:
                    alpha = pixel[3]
                except IndexError:
                    alpha = 255

                if alpha < 128:
                    row += " "
                    color_data[Vec2(x, y)] = NONE_COLOR
                    continue
                color = Color(int(pixel[0]), int(pixel[1]), int(pixel[2]))
                color_data[Vec2(x, y)] = color
                char = self.color_to_char.get(color, self.default_char)
                row += char
            char_data.append(row)

        return char_data, color_data

    def _validate_color_mode(self):
        if not (self.color_mode == "foreground" or self.color_mode == "background"):
            raise Exception(f"Invalid color mode {self.color_mode}, valid modes: [foreground, background]")

    def __str__(self):
        return f"Texture(texture_location={self.texture_location},color_mode={self.color_mode},color_to_char={self.color_to_char})"

class TextureLoader:
    textures: dict[str, Texture] = dict()

    @staticmethod
    def load():
        TextureLoader._load_dir("res/texture")

    @staticmethod
    def _load_file(directory: str, file: str):
        if not file.endswith(".json"): return

        texture_id = (directory + "/" + file).removeprefix("res/").removesuffix(".json")
        print(f"found texture file: {file}, assigned id: {texture_id}")
        TextureLoader.textures[texture_id] = Texture(os.path.join(directory, file))

    @staticmethod
    def _load_dir(directory: str):
        print(f"loading textures from {directory}")
        for root, dirs, files in os.walk(directory):
            for file in files:
                TextureLoader._load_file(root, file)
            for sub_dir in dirs:
                TextureLoader._load_dir(directory + "/" + sub_dir)
