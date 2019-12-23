# coding=utf-8
from typing import List, Type

from afol_toolbox_app.model import util


class Gear(object):
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

    @staticmethod
    def get_all() -> List:
        return NormalGear.get_all() + WormGear.get_all() + TurntableGear.get_all()

    @staticmethod
    def can_be_driver_of(follower) -> bool:
        follower_cls = util.get_class(follower, Gear)
        if follower_cls == WormGear:  # no gear can drive a worm gear
            return False
        else:
            return True

    @classmethod
    def can_be_follower_of(cls, driver):
        driver_cls = util.get_class(driver, Gear)
        return driver_cls.can_be_driver_of(cls)


class NormalGear(Gear):
    def __init__(self, teeth: int):
        super().__init__(teeth=teeth, image_name=f"{teeth}T.png")

    @staticmethod
    def get_all() -> List[Type[Gear]]:
        return [Gear8, Gear12, Gear16, Gear20, Gear24, Gear28, Gear36, Gear40]


class TurntableGear(Gear):
    def __init__(self, teeth):
        super().__init__(teeth=teeth, image_name=f"{teeth}T_Turntable.png")

    @staticmethod
    def get_all() -> List[Type[Gear]]:
        return [TurntableGear28, TurntableGear56, TurntableGear60]


class Gear8(NormalGear):
    def __init__(self):
        super().__init__(8)


class Gear12(NormalGear):
    def __init__(self):
        super().__init__(12)


class Gear16(NormalGear):
    def __init__(self):
        super().__init__(16)


class Gear20(NormalGear):
    def __init__(self):
        super().__init__(20)


class Gear24(NormalGear):
    def __init__(self):
        super().__init__(24)


class Gear28(NormalGear):
    def __init__(self):
        super().__init__(28)


class Gear36(NormalGear):
    def __init__(self):
        super().__init__(36)


class Gear40(NormalGear):
    def __init__(self):
        super().__init__(40)


class TurntableGear28(TurntableGear):
    def __init__(self):
        super().__init__(28)


class TurntableGear56(TurntableGear):
    def __init__(self):
        super().__init__(56)


class TurntableGear60(TurntableGear):
    def __init__(self):
        super().__init__(60)


class WormGear(Gear):
    def __init__(self):
        super().__init__(teeth=1, image_name="1T.png")

    @staticmethod
    def get_all() -> List[Type[Gear]]:
        return [WormGear]
