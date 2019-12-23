# coding=utf-8
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


class TestUtil(TestCase):
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
