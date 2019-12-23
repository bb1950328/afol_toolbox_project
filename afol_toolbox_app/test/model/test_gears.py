from unittest import TestCase

# coding=utf-8
from afol_toolbox_app.model.gears import Gear8, Gear16, TurntableGear60, WormGear, Gear, NormalGear, GearCombination, \
    GearRatio


class TestGears(TestCase):
    def test_can_be_driver_of(self):
        self.assertTrue(Gear8.can_be_driver_of(Gear16))
        self.assertTrue(Gear8.can_be_driver_of(Gear8))
        self.assertTrue(TurntableGear60.can_be_driver_of(Gear8))
        self.assertTrue(WormGear.can_be_driver_of(Gear8))
        self.assertFalse(Gear8.can_be_driver_of(WormGear))

    def test_can_be_follower_of(self):
        self.assertTrue(Gear16.can_be_follower_of(Gear8))
        self.assertTrue(Gear16.can_be_follower_of(WormGear))
        self.assertFalse(WormGear.can_be_follower_of(Gear8))

    def test_teeth(self):
        self.assertEqual(8, Gear8.gi().teeth)
        self.assertEqual(1234, Gear(1234, "").teeth)

    def test_image_name(self):
        self.assertEqual("1234T.png", NormalGear(1234).image_name)

    def test_str(self):
        self.assertEqual("Gear", str(Gear.gi(1234, "")))
        self.assertEqual("Gear8", str(Gear8.gi()))

    def test_gear_combination1(self):
        co = GearCombination(Gear8.gi(), Gear16.gi())
        self.assertEqual(Gear8.gi(), co.driver)
        self.assertEqual(Gear16.gi(), co.follower)

    def test_gear_combination2(self):
        co = GearCombination(Gear8.gi(), Gear16.gi())
        expected_ratio = GearRatio.of_gears(Gear8.gi(), Gear16.gi())
        self.assertEqual(expected_ratio, co.ratio)

    def test_gear_combination3(self):
        with self.assertRaises(ValueError):
            GearCombination(Gear8.gi(), WormGear.gi())

    def test_gear_ratio1(self):
        ra = GearRatio.of_gears(Gear16.gi(), Gear8.gi())
        self.assertEqual("GearRatio[2:1]", str(ra))

    def test_gear_ratio2(self):
        ra = GearRatio.of_gears(Gear16.gi(), Gear8.gi())
        self.assertEqual(2, ra.a)
        self.assertEqual(1, ra.b)

    def test_gear_ratio3(self):
        ra = GearRatio.of_gears(Gear16.gi(), Gear8.gi())
        self.assertTrue(ra.is_speed_increased())
        self.assertFalse(ra.is_speed_decreased())
        self.assertTrue(ra.is_torque_decreased())
        self.assertFalse(ra.is_torque_increased())
        self.assertFalse(ra.is_1to1())

    def test_gear_ratio4(self):
        ra = GearRatio.of_gears(Gear16.gi(), Gear16.gi())
        self.assertFalse(ra.is_speed_increased())
        self.assertFalse(ra.is_speed_decreased())
        self.assertFalse(ra.is_torque_decreased())
        self.assertFalse(ra.is_torque_increased())
        self.assertTrue(ra.is_1to1())
