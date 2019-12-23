# coding=utf-8
from afol_toolbox_app.model.gears.normal_gear import NormalGear


class Gear16(NormalGear):
    def __init__(self):
        super().__init__(16)