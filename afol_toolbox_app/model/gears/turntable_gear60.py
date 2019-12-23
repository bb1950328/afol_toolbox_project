# coding=utf-8
from afol_toolbox_app.model.gears.turntable_gear import TurntableGear


class TurntableGear60(TurntableGear):
    def __init__(self):
        super().__init__(60)