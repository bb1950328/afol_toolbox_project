# coding=utf-8
from decimal import Decimal
from typing import Dict, Union, Tuple


def get_class(object_or_class, min_base_class=object):
    if object_or_class.__class__ != type:
        object_or_class = object_or_class.__class__
    if not issubclass(object_or_class, min_base_class):
        raise ValueError(f"{object_or_class} isn't a subclass of {min_base_class} !")
    return object_or_class


class Singleton(object):
    """
    inherit from this class to add a singleton functionality
    """
    _instances: Dict[type, object] = {}

    @classmethod
    def get_instance(cls, *args, **kwargs):
        """
        Example: (A extends Singleton, B extends A)
        A.get_instance() -> <A object at 0xAAAAAAAA>
        B.get_instance() -> <B object at 0xBBBBBBBB>
        A.get_instance() -> <A object at 0xAAAAAAAA> # the same as from the first call
        pass arguments for __init__(*args, **kwargs) as *args and *kwargs, if needed
        """
        if cls not in cls._instances.keys():
            # noinspection PyArgumentList
            cls._instances[cls] = cls(*args, **kwargs)
        return cls._instances[cls]

    @classmethod
    def gi(cls, *args, **kwargs):
        """
        the same as get_instance(), but shorter name
        """
        return cls.get_instance(*args, **kwargs)


def expand_to_int_fraction(a: Union[int, float, Decimal], b: Union[int, float, Decimal]) -> Tuple[int, int]:
    """
    1, 2.5 -> 2, 5
    1, 2 -> 1, 2
    """
    if not (isinstance(a, int) and isinstance(b, int)):
        if isinstance(a, (float, int)):
            a = Decimal(a)
        if isinstance(b, (float, int)):
            b = Decimal(b)
        ratio = a / b
        return ratio.as_integer_ratio()
    else:
        return a, b


def shorten_fraction(a, b):
    primes = get_prime_numbers_until(min(a, b) + 1)
    for num in primes:
        if a < num or b < num:
            break
        a_bak = a
        b_bak = b
        while (not a % 1) and (not b % 1):
            a_bak = a
            b_bak = b
            a /= num
            b /= num
        a = a_bak
        b = b_bak
    return int(a), int(b)


def get_prime_numbers_until(until: int):
    result = [1 for i in range(until)]
    for i in range(2, int(until)):
        x = 2 * i
        while x < until:
            result[x] = 0
            x += i
    return [num for num in range(until) if result[num]][2:]
