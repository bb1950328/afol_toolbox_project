# coding=utf-8
from afol_toolbox_app.model.gears.gear import Gear


class WormGear(Gear):
    def __init__(self):
        super().__init__(teeth=1, image_name="1T.png")