# coding=utf-8
from abc import ABC


class Gear(object, ABC):
    _teeth: int
    _image_name: str

    @property
    def teeth(self):
        return self._teeth

    @property
    def image_name(self):
        return self._image_name

    def __init__(self, teeth: int, image_name: str):
        self._teeth = teeth
        self._image_name = image_name
