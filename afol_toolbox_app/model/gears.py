# coding=utf-8
import itertools
import cachetools.func
import math
import os
from abc import ABC
from decimal import Decimal
from typing import List, Type, Union, Optional, Set, Iterable, Tuple

from afol_toolbox_app.model import util


class GearData(util.CSVDict, util.Singleton):
    def __init__(self):
        path = os.path.join(os.path.dirname(__file__), "gear_data.csv")
        super().__init__(path, "Name", has_type_row=True)


class Gear(util.Singleton):
    class GearFilter(util.Filter, ABC):
        pass

    class AllGearsFilter(GearFilter, util.Singleton):

        def accept(self, obj: object) -> bool:
            return True

    class TeethLimitGearFilter(GearFilter):
        _min: int
        _max: int

        # noinspection PyShadowingBuiltins
        def __init__(self, *, min=0, max=10 ** 10):
            self._min = min
            self._max = max

        def accept(self, obj: object) -> bool:
            return isinstance(obj, Gear) and self._min <= obj.teeth <= self._max

    _teeth: int

    @property
    def teeth(self):
        return self._teeth

    @property
    def category(self):
        return "Gear"

    @property
    def display_name(self):
        return f"{self.category} {self.teeth}T"

    @property
    def data(self) -> dict:
        return GearData.gi()[self.__class__.__name__]

    @property
    def image_name(self) -> str:
        return self.data["ImgName"]

    @property
    def radius_in_mm(self) -> int:
        return self.data["RadiusMM"]

    def __init__(self, teeth: int):
        self._teeth = teeth

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
    @cachetools.func.lfu_cache(maxsize=256)
    def with_num_teeth(cls, num_teeth) -> List[Type]:
        result = []
        for gear in cls.get_all():
            if gear.gi().teeth == num_teeth:
                result.append(gear)
        return result

    @classmethod
    @cachetools.func.lfu_cache(maxsize=256)
    def nearest_with_num_teeth(cls, num_teeth, skip_worm_gear: bool = False) -> Type:
        result = None
        dev = -1
        all_gears = cls.get_all()
        if skip_worm_gear:
            all_gears.remove(WormGear)
        for gear in all_gears:
            gdev = abs(gear.gi().teeth - num_teeth)
            if dev == -1 or dev > gdev:
                dev = gdev
                result = gear
        return result

    def __str__(self):
        return self.__class__.__name__

    def __repr__(self) -> str:
        return str(self) + ".gi()"

    def __eq__(self, other):
        return isinstance(other, Gear) and self.teeth == other.teeth and self.image_name == other.image_name

    def __hash__(self) -> int:
        return hash(str(self))


class NormalGear(Gear):
    class NormalGearsOnlyFilter(Gear.GearFilter, util.Singleton):

        def accept(self, obj: object) -> bool:
            return obj.__class__ in NormalGear.get_all() or any(isinstance(obj, cls) for cls in NormalGear.get_all())

    def __init__(self, teeth: int):
        super().__init__(teeth=teeth)

    @staticmethod
    def get_all() -> List[Type[Gear]]:
        return [Gear8, Gear12, Gear16, Gear20, Gear24, Gear28, Gear36, Gear40]


class TurntableGear(Gear):
    def __init__(self, teeth):
        super().__init__(teeth=teeth)

    @property
    def category(self):
        return "Turntable"

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
        super().__init__(teeth=1)

    @property
    def category(self):
        return "Worm Gear"

    @property
    def display_name(self):
        return f"Worm Gear"

    @staticmethod
    def get_all() -> List[Type[Gear]]:
        return [WormGear]


class GearCombination(object):
    class GearCombinationFilter(util.Filter, ABC):
        pass

    class AllGearCombinationsFilter(GearCombinationFilter, util.Singleton):

        def accept(self, obj: object) -> bool:
            return True

    class No1to1GearCombinationFilter(GearCombinationFilter):

        def accept(self, obj: object) -> bool:
            return isinstance(obj, GearCombination) and obj.driver.teeth != obj.follower.teeth  # todo testing

    class PossibleOnLiftbeamCombinationFilter(GearCombinationFilter):

        def accept(self, obj) -> bool:
            return isinstance(obj, GearCombination) \
                   and obj.axle_distance_mm % 8 == 0 \
                   and not isinstance(obj.driver, WormGear)
            # todo testing

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

    @property
    def axle_distance_mm(self) -> int:
        return self.driver.radius_in_mm + self.follower.radius_in_mm

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

    def __str__(self) -> str:
        return f"GearCombination[{self.driver}:{self.follower}]"

    def __repr__(self) -> str:
        return f"GearCombination({self.driver}.gi(), {self.follower}.gi())"

    def __eq__(self, other) -> bool:
        return isinstance(other, GearCombination) and self.driver == other.driver and self.follower == other.follower

    def __hash__(self) -> int:
        return hash(str(self))


class GearRatio(object):
    """
    class to represent a gear ratio
    when a is 2 and b is 5, that means that torque is increased 2.5 times and speed is decreased 2.5 times
    """

    class GearRatioFilter(util.Filter, ABC):
        pass

    class AllGearRatiosFilter(GearRatioFilter, util.Singleton):

        def accept(self, obj: object) -> bool:
            return True

    class NotBiggerThanGearRatioFilter(GearRatioFilter):  # todo testing
        def __init__(self, a, b):
            self.value = a / b
            if self.value < 1:
                self.value = 1 / self.value

        def accept(self, obj: object) -> bool:
            if isinstance(obj, GearRatio):
                ov = obj.a / obj.b
                if ov < 1:
                    ov = 1 / ov
                return ov <= self.value

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
        self._a, self._b = util.shorten_fraction(self._a, self._b)

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

    @staticmethod
    def of_combination_chain(it: Iterable[GearCombination]):
        aa = 1
        bb = 1
        for combi in it:
            ratio = combi.ratio
            aa *= ratio._a
            bb *= ratio._b
        return GearRatio.of_int_ratio(aa, bb)

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

    def deviation_to(self, other_ratio):
        ra = (self.a / self.b)
        rb = (other_ratio.a / other_ratio.b)
        return max(ra / rb, rb / ra) - 1

    def __str__(self) -> str:
        return f"GearRatio[{self.a}:{self.b}]"

    def __eq__(self, o: object) -> bool:
        return isinstance(o, GearRatio) and o.a == self.a and o.b == self.b

    def __mul__(self, other):
        if not isinstance(other, GearRatio):
            raise ValueError("Can only multiply with GearRatio!!")
        return GearRatio.of_int_ratio(self.a * other.a, self.b * other.b)

    def __hash__(self) -> int:
        return hash(str(self))


class CombinationFinder(object):
    @staticmethod
    @cachetools.func.lfu_cache(maxsize=256)
    def all_combinations(ratio: GearRatio) -> List[GearCombination]:
        result = []
        for driver in Gear.get_all():
            follower_teeth = driver.gi().teeth / ratio.a * ratio.b
            if follower_teeth == 1 or follower_teeth % 1:
                # worm gear can't be follower and teeth can't be decimal number
                continue
            followers = Gear.with_num_teeth(follower_teeth)
            for fo in followers:
                # noinspection PyUnresolvedReferences
                result.append(GearCombination(driver.gi(), fo.gi()))
        return result

    @staticmethod
    @cachetools.func.lfu_cache(maxsize=256)
    def nearest_combinations(ratio: GearRatio) -> List[GearCombination]:
        result = []
        dev = -1
        for driver in Gear.get_all():
            follower_teeth = driver.gi().teeth / ratio.a * ratio.b
            # noinspection PyUnresolvedReferences
            follower = Gear.nearest_with_num_teeth(follower_teeth, skip_worm_gear=True).gi()
            fra = GearRatio.of_gears(driver.gi(), follower)
            fra_dev = ratio.deviation_to(fra)
            if dev == -1 or fra_dev < dev:
                result = [GearCombination(driver.gi(), follower)]
                dev = fra_dev
            elif math.isclose(dev, fra_dev):
                result.append(GearCombination(driver.gi(), follower))
        return result

    @staticmethod
    @cachetools.func.lfu_cache(maxsize=256)
    def all_possible_combinations(gear_filter: Gear.GearFilter = Gear.AllGearsFilter.gi()) -> List[GearCombination]:
        result = []
        for driver in Gear.get_all():
            if gear_filter.accept(driver.gi()):
                for follower in Gear.get_all():
                    if follower == WormGear or not gear_filter.accept(follower.gi()):
                        continue
                    result.append(GearCombination(driver.gi(), follower.gi()))
        return result

    @staticmethod
    def clean_combination_chain(chain: Union[List[GearCombination], Tuple[GearCombination]]) -> Set[GearCombination]:
        return set(chain)

    @staticmethod
    @cachetools.func.lfu_cache(maxsize=256)
    def all_combination_chains(
            ratio: GearRatio,
            max_results: int = 100,
            max_chain_length: int = 5,
            max_deviation: float = 0.1,
            gear_filter: Gear.GearFilter = Gear.AllGearsFilter.gi(),
            ratio_filter: GearRatio.GearRatioFilter = GearRatio.AllGearRatiosFilter.gi(),
            combination_fltr: GearCombination.GearCombinationFilter = GearCombination.AllGearCombinationsFilter.gi()) \
            -> List[Tuple[float, Set[GearCombination]]]:
        """
        max_deviation: 0.01 = 1%
        returns a list of (deviation, set of combinations) tuples
        """
        result = []
        all_possible = CombinationFinder.all_possible_combinations(gear_filter)
        combination_fltr += GearCombination.No1to1GearCombinationFilter()
        all_possible = [combi for combi in all_possible
                        if combination_fltr.accept(combi) and ratio_filter.accept(combi.ratio)]
        for chain_length in range(1, max_chain_length + 1):
            for combi in itertools.combinations_with_replacement(all_possible, chain_length):
                oldlen = len(combi)
                combi = CombinationFinder.clean_combination_chain(combi)
                if len(combi) < oldlen:
                    continue
                combi_ratio = GearRatio.of_combination_chain(combi)
                dev = ratio.deviation_to(combi_ratio)
                if dev < max_deviation:
                    result.append((dev, combi))
        result.sort(key=lambda x: x[0])
        if len(result) > max_results:
            result = result[0:max_results]
        return result
