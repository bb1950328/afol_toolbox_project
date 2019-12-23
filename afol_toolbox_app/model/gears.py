# coding=utf-8
from decimal import Decimal
from typing import List, Type, Union, Optional

from afol_toolbox_app.model import util


class Gear(util.Singleton):
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

    @classmethod
    def with_num_teeth(cls, num_teeth) -> Optional[Type]:
        for gear in cls.get_all():
            if gear.gi().teeth == num_teeth:
                return gear
        return None

    def __str__(self):
        return self.__class__.__name__


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


class GearCombination(object):
    def __init__(self, driver: Gear, follower: Gear):
        self.driver = driver
        self.follower = follower

    _driver: Gear
    _follower: Gear
    _ratio: Optional[object]  # GearRatio

    @property
    def driver(self) -> Gear:
        return self._driver

    @property
    def follower(self) -> Gear:
        return self._follower

    @property
    def ratio(self):
        if self._ratio is None:
            self._ratio = GearRatio.of_gears(self._driver, self._follower)
        return self._ratio

    @driver.setter
    def driver(self, driver: Gear):
        self._driver = driver
        self._ratio = None

    @follower.setter
    def follower(self, follower: Gear):
        if isinstance(follower, WormGear):
            raise ValueError("WormGear can't be follower!!!")
        self._follower = follower
        self._ratio = None

    def __str__(self):
        return f"GearCombination[{self.driver}:{self.follower}]"


class GearRatio(object):
    """
    class to represent a gear ratio
    when a is 2 and b is 5, that means that torque is increased 2.5 times and speed is decreased 2.5 times
    """

    def __init__(self):
        self._a = 1
        self._b = 1

    _a: int
    _b: int

    @property
    def a(self):
        return self._a

    @property
    def b(self):
        return self._b

    @a.setter
    def a(self, a):
        if isinstance(a, float):
            a, b = util.expand_to_int_fraction(a, self.b)
            self.b = b
        self._a = a
        self._divide_if_possible()

    @b.setter
    def b(self, b):
        if isinstance(b, float):
            a, b = util.expand_to_int_fraction(self.a, b)
            self.a = a
        self._b = b
        self._divide_if_possible()

    def _divide_if_possible(self):
        self._a, self._b = (Decimal(self.a) / Decimal(self.b)).as_integer_ratio()

    @property
    def ratio(self):
        return self._a, self._b

    @staticmethod
    def of_int_ratio(a: int, b: int):
        obj = GearRatio()
        obj.a = a
        obj.b = b
        return obj

    @staticmethod
    def of_ratio(a: Union[int, float, Decimal], b: Union[int, float, Decimal]):
        return GearRatio.of_int_ratio(*util.expand_to_int_fraction(a, b))

    @staticmethod
    def of_gears(driver: Gear, follower: Gear):
        if not driver.can_be_driver_of(follower):
            raise ValueError(f"{driver} can't be driver of {follower}!!!")
        return GearRatio.of_int_ratio(driver.teeth, follower.teeth)

    def is_torque_increased(self) -> bool:
        return self.a < self.b

    def is_torque_decreased(self) -> bool:
        return self.a > self.b

    def is_speed_increased(self) -> bool:
        return self.a > self.b

    def is_speed_decreased(self) -> bool:
        return self.a < self.b

    def is_1to1(self) -> bool:
        return self.a == self.b == 1

    def __str__(self) -> str:
        return f"GearRatio[{self.a}:{self.b}]"

    def __eq__(self, o: object) -> bool:
        return isinstance(o, GearRatio) and o.a == self.a and o.b == self.b


class RatioFinder(object):
    @staticmethod
    def find_all_combinations(ratio: GearRatio):
        result = []
        for driver in Gear.get_all():
            follower_teeth = driver.teeth / ratio.a * ratio.b
            if follower_teeth == 1 or follower_teeth % 1:
                # wormgear can't be follower and teeth can't be decimal number
                continue
            follower = Gear.with_num_teeth(follower_teeth)
            if isinstance(follower, Gear):
                result.append(GearCombination(driver.gi(), follower.gi()))
        return result
