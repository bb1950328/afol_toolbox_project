# coding=utf-8
import os
import pathlib
import random
import shutil
import time
from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Dict, Union, Tuple, Callable, Iterable

ALPHANUM_CHARS = "abcdefghijklmnopqrstuvwxyz0123456789"


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


def has_comma(num: Union[Decimal, float]) -> bool:
    if isinstance(num, float):
        num = Decimal(num)
    return num.as_integer_ratio()[1] != 1


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
        factor = 1
        while (has_comma(a) or has_comma(b)) and factor < 999_999_999:
            a *= 10
            b *= 10
            factor *= 10
        return shorten_fraction(int(a), int(b))
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


class Filter(ABC):
    @abstractmethod
    def accept(self, obj: object) -> bool:
        pass

    @classmethod
    def of_whitelist(cls, whitelist):
        fi = cls()
        fi.accept = lambda obj: obj in whitelist
        return fi

    @classmethod
    def of_blacklist(cls, blacklist):
        fi = cls()
        fi.accept = lambda obj: obj not in blacklist
        return fi

    def __add__(self, other):
        class SumFilter(Filter):
            def accept(self, obj: object) -> bool:
                return all(fi.accept(obj) for fi in self._subfilters)

            def __init__(self, subfilters: Iterable[Filter]):
                self._subfilters = subfilters

        return SumFilter([self, other])


type_funcs: Dict[str, Callable] = {
    "bool": bool,
    "int": int,
    "float": float,
    "decimal": Decimal,
    "str": str,
    "text": str,
}


class CSVDict(dict):
    def __init__(self, filename: str, key_column=None, delimiter=";", has_type_row=False):
        """
        filename: path to open
        key_column: name of the column which has the keys, None->first colummn
        delimiter: character between two columns
        has_type_row: if True, second row includes data types, like str;int;float;decimal
        """
        super().__init__()
        with open(filename, "r") as f:
            headers = f.readline().strip().split(delimiter)
            key_idx = 0 if key_column is None else headers.index(key_column)
            if has_type_row:
                types = f.readline().strip().split(delimiter)
                types = [type_funcs[t] for t in types]
            for row in f.readlines():
                values = row.strip().split(";")
                row_dict = dict()
                for col_idx, val in enumerate(values):
                    if has_type_row:
                        val = types[col_idx](val)
                    if col_idx == key_idx:
                        key = val
                    else:
                        row_dict[headers[col_idx]] = val
                self[key] = row_dict


def get_arg_hash(args: Iterable, kwargs: Dict):
    ha = hash(args)
    for k, v in kwargs.items():
        ha += hash(k)
        ha += hash(k) * hash(v)
    return hash(ha)


def get_execution_time(func, *args, **kwargs):
    start = time.perf_counter()
    func(*args, **kwargs)
    end = time.perf_counter()
    return end - start


def get_random_alphanumeric_string(length: int = 10):
    chars = [ALPHANUM_CHARS[random.randint(0, 35)] for i in range(length)]
    return "".join(chars)


def get_all_files_in_directory(start=".", absolute=False):
    result = []
    for path, subdirs, files in os.walk(start):
        result += [os.path.join(path, fname) for fname in files]
    if absolute:
        result = [os.path.abspath(rel) for rel in result]
    return result


def create_containing_folders_if_necessary(filepath: str) -> None:
    pathlib.Path(os.path.dirname(filepath)).mkdir(parents=True, exist_ok=True)


def clear_folder_content(folder: str):
    for filename in os.listdir(folder):
        filepath = os.path.join(folder, filename)
        try:
            shutil.rmtree(filepath)
        except OSError:
            os.remove(filepath)
