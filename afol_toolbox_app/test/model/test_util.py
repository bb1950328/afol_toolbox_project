# coding=utf-8
import decimal
import time
from unittest import TestCase

from afol_toolbox_app.model import util


class Dummy(object):
    pass


class SubDummy(Dummy):
    pass


class SiDummy(util.Singleton):
    pass


class SubSiDummy(SiDummy):
    pass


class NotAbstractFilter(util.Filter):

    def accept(self, obj: object) -> bool:
        raise ValueError("should not call this!!!")


class TestUtil(TestCase):

    def setUp(self) -> None:
        pass

    def test_get_class_class1(self):
        self.assertEqual(Dummy, util.get_class(Dummy))

    def test_get_class_class2(self):
        self.assertEqual(SubDummy, util.get_class(SubDummy, Dummy))

    def test_get_class_class3(self):
        with self.assertRaises(ValueError):
            util.get_class(Dummy, SubDummy)

    def test_get_class_instance1(self):
        self.assertEqual(Dummy, util.get_class(Dummy()))

    def test_get_class_instance2(self):
        self.assertEqual(SubDummy, util.get_class(SubDummy(), Dummy))

    def test_get_class_instance3(self):
        with self.assertRaises(ValueError):
            util.get_class(Dummy(), SubDummy)

    def test_singleton1(self):
        sd = SiDummy.get_instance()
        self.assertEqual(SiDummy, sd.__class__)

    def test_singleton2(self):
        ssd = SubSiDummy.get_instance()
        self.assertEqual(SubSiDummy, ssd.__class__)

    def test_singleton3(self):
        sd = SiDummy.get_instance()
        sd2 = SiDummy.get_instance()
        self.assertEqual(sd, sd2)

    def test_singleton4(self):
        ssd = SubSiDummy.get_instance()
        ssd2 = SubSiDummy.get_instance()
        self.assertEqual(ssd, ssd2)

    def test_shorten_fraction1(self):
        self.assertEqual((1, 1), util.shorten_fraction(1, 1))
        self.assertEqual((1, 1), util.shorten_fraction(2, 2))
        self.assertEqual((1, 1), util.shorten_fraction(123, 123))

    def test_shorten_fraction2(self):
        self.assertEqual((1, 2), util.shorten_fraction(1, 2))
        self.assertEqual((1, 2), util.shorten_fraction(2, 4))
        self.assertEqual((1, 2), util.shorten_fraction(123, 123 * 2))

    def test_shorten_fraction3(self):
        self.assertEqual((22, 7), util.shorten_fraction(88, 28))
        self.assertEqual((1, 3), util.shorten_fraction(15, 45))

    def test_get_prime_numbers_until(self):
        expected = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
        actual = util.get_prime_numbers_until(100)
        self.assertEqual(expected, actual)

    def test_get_arg_hash(self):
        ha = [
            util.get_arg_hash((1, 2, 3), {"hello": 123, "world": 321}),
            util.get_arg_hash((3, 2, 1), {"hello": 123, "world": 321}),
            util.get_arg_hash((3, 2, 1), {"hell": 123, "world": 321}),
            util.get_arg_hash((3, 2, 1), {"hello": 33, "world": 321}),
            util.get_arg_hash((3, 2, 2), {"hello": 34, "world": 321}),
            util.get_arg_hash((3, 2, 2), {"hello": 34}),
            util.get_arg_hash((3, 2, 2, 234), {"hello": 34}),
            util.get_arg_hash((), {"hello": 34}),
            util.get_arg_hash((3, 2, 2, 234), dict()),
            util.get_arg_hash(tuple(), dict()),
        ]
        no_duplicates = list(set(ha))
        self.assertEqual(sorted(ha), sorted(no_duplicates))

    def test_expand_to_int_fraction1(self):
        self.assertEqual((1, 2), util.expand_to_int_fraction(0.5, 1))

    def test_expand_to_int_fraction2(self):
        self.assertEqual((1, 4), util.expand_to_int_fraction(5.5, 22))

    def test_expand_to_int_fraction3(self):
        self.assertEqual((37, 60), util.expand_to_int_fraction(decimal.Decimal("3.7"), 6))

    def test_expand_to_int_fraction4(self):
        self.assertEqual((1, 5), util.expand_to_int_fraction(decimal.Decimal("1.234"), decimal.Decimal("6.17")))

    def test_expand_to_int_fraction5(self):
        self.assertEqual((1, 5), util.expand_to_int_fraction(1, 5))

    def test_filter_whitelist(self):
        fi = NotAbstractFilter.of_whitelist([1, 3, 5])
        self.assertTrue(fi.accept(1))
        self.assertFalse(fi.accept(2))
        self.assertTrue(fi.accept(3))
        self.assertFalse(fi.accept(4))
        self.assertTrue(fi.accept(5))

    def test_filter_blacklist(self):
        fi = NotAbstractFilter.of_blacklist([1, 3, 5])
        self.assertFalse(fi.accept(1))
        self.assertTrue(fi.accept(2))
        self.assertFalse(fi.accept(3))
        self.assertTrue(fi.accept(4))
        self.assertFalse(fi.accept(5))

    def test_get_execution_time(self):
        expected = 0.5
        actual = util.get_execution_time(lambda: time.sleep(expected))
        self.assertAlmostEqual(expected, actual, delta=0.01)

    def test_get_random_string(self):
        res = util.get_random_alphanumeric_string(length=20)
        self.assertEqual(20, len(res))
        self.assertNotIn(" ", res)
        for char in res:
            is_num = ord("0") <= ord(char) <= ord("9")
            is_lower_alpha = ord("a") <= ord(char) <= ord("z")
            self.assertTrue(is_num or is_lower_alpha)
