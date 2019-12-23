# coding=utf-8
from abc import ABC

from afol_toolbox_app.model.gears.gear import Gear


class TurntableGear(Gear, ABC):
    def __init__(self, teeth):
        super().__init__(teeth=teeth, image_name=f"{teeth}T_Turntable.png")