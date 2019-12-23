# coding=utf-8
from abc import ABC

from afol_toolbox_app.model.gears.gear import Gear


class NormalGear(Gear, ABC):
    def __init__(self, teeth: int):
        super().__init__(teeth=teeth, image_name=f"{teeth}T.png")