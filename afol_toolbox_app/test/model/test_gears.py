from unittest import TestCase

# coding=utf-8
from afol_toolbox_app.model import util
from afol_toolbox_app.model.gears import Gear8, Gear16, TurntableGear60, WormGear, Gear, GearCombination, \
    GearRatio, CombinationFinder, Gear12, Gear20, Gear28, TurntableGear28, TurntableGear56, Gear40, Gear24, Gear36, \
    NormalGear
from afol_toolbox_app.test.model import results


class TestGears(TestCase):

    def setUp(self) -> None:
        pass

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
        self.assertEqual(1234, Gear(1234).teeth)

    def test_image_name(self):
        self.assertEqual("8T.svg", Gear8.gi().image_name)
        self.assertEqual("56T_Turntable.svg", TurntableGear56.gi().image_name)

    def test_radius(self):
        self.assertEqual(4, Gear8.gi().radius_in_mm)
        self.assertEqual(34, TurntableGear56.gi().radius_in_mm)

    def test_str(self):
        self.assertEqual("Gear", str(Gear.gi(1234)))
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

    def test_gear_deviation_to1(self):
        ra1 = GearRatio.of_int_ratio(123, 321)
        ra2 = GearRatio.of_int_ratio(1234, 3250)
        de1 = ra1.deviation_to(ra2)
        de2 = ra2.deviation_to(ra1)
        self.assertAlmostEqual(de1, de2)
        self.assertAlmostEqual(0.00917917569, de1)

    def test_gear_deviation_to2(self):
        ra1 = GearRatio.of_int_ratio(1, 2)
        ra2 = GearRatio.of_int_ratio(1, 3)
        de1 = ra1.deviation_to(ra2)
        de2 = ra2.deviation_to(ra1)
        self.assertAlmostEqual(de1, de2)
        self.assertAlmostEqual(0.5, de1)

    def test_gear_deviation_to3(self):
        ra1 = GearRatio.of_int_ratio(1, 2)
        ra2 = GearRatio.of_int_ratio(1, 2)
        de1 = ra1.deviation_to(ra2)
        de2 = ra2.deviation_to(ra1)
        self.assertAlmostEqual(de1, de2)
        self.assertAlmostEqual(0, de1)

    def test_combinationfinder_all_combinations1(self):
        expected = [
            GearCombination(Gear8.gi(), Gear16.gi()),
            GearCombination(Gear12.gi(), Gear24.gi()),
            GearCombination(Gear20.gi(), Gear40.gi()),
            GearCombination(Gear28.gi(), TurntableGear56.gi()),
            GearCombination(TurntableGear28.gi(), TurntableGear56.gi()),
        ]
        actual = CombinationFinder.all_combinations(GearRatio.of_int_ratio(1, 2))
        self.assertEqual(expected, actual)

    def test_combinationfinder_all_combinations2(self):
        expected = [
            GearCombination(Gear8.gi(), Gear24.gi()),
            GearCombination(Gear12.gi(), Gear36.gi()),
            GearCombination(Gear20.gi(), TurntableGear60.gi()),
        ]
        actual = CombinationFinder.all_combinations(GearRatio.of_int_ratio(1, 3))
        self.assertEqual(expected, actual)

    def test_combinationfinder_all_combinations3(self):
        expected = [
            GearCombination(Gear8.gi(), Gear8.gi()),
            GearCombination(Gear12.gi(), Gear12.gi()),
            GearCombination(Gear16.gi(), Gear16.gi()),
            GearCombination(Gear20.gi(), Gear20.gi()),
            GearCombination(Gear24.gi(), Gear24.gi()),
            GearCombination(Gear28.gi(), Gear28.gi()),
            GearCombination(Gear28.gi(), TurntableGear28.gi()),
            GearCombination(Gear36.gi(), Gear36.gi()),
            GearCombination(Gear40.gi(), Gear40.gi()),
            GearCombination(TurntableGear28.gi(), Gear28.gi()),
            GearCombination(TurntableGear28.gi(), TurntableGear28.gi()),
            GearCombination(TurntableGear56.gi(), TurntableGear56.gi()),
            GearCombination(TurntableGear60.gi(), TurntableGear60.gi()),
        ]
        actual = CombinationFinder.all_combinations(GearRatio.of_int_ratio(1, 1))
        self.assertEqual(expected, actual)

    def test_combinationfinder_nearest_combinations1(self):
        expected = [
            GearCombination(Gear20.gi(), Gear28.gi()),
            GearCombination(Gear40.gi(), TurntableGear56.gi()),
        ]
        actual = CombinationFinder.nearest_combinations(GearRatio.of_int_ratio(5, 7))
        self.assertEqual(expected, actual)

    def test_combinationfinder_nearest_combinations2(self):
        expected = [
            GearCombination(Gear36.gi(), Gear28.gi()),
        ]
        actual = CombinationFinder.nearest_combinations(GearRatio.of_int_ratio(9, 7))
        self.assertEqual(expected, actual)

    def test_combinationfinder_nearest_combinations3(self):
        expected = [
            GearCombination(TurntableGear60.gi(), Gear8.gi()),
        ]
        actual = CombinationFinder.nearest_combinations(GearRatio.of_int_ratio(100, 1))
        self.assertEqual(expected, actual)

    def test_combinationfinder_nearest_combinations4(self):
        expected = [
            GearCombination(WormGear.gi(), TurntableGear60.gi()),
        ]
        actual = CombinationFinder.nearest_combinations(GearRatio.of_int_ratio(1, 100))
        self.assertEqual(expected, actual)

    def test_combinationfinder_all_possible_combinations1(self):
        expected = results.ALL_POSSIBLE_COMBINATIONS_1
        actual = CombinationFinder.all_possible_combinations()
        self.assertEqual(expected, actual)

    def test_combinationfinder_all_possible_combinations2(self):
        expected = results.ALL_POSSIBLE_COMBINATIONS_2
        actual = CombinationFinder.all_possible_combinations(NormalGear.NormalGearsOnlyFilter.gi())
        self.assertEqual(expected, actual)

    def test_combinationfinder_all_possible_combinations3(self):
        expected = results.ALL_POSSIBLE_COMBINATIONS_3
        gear_filter = NormalGear.NormalGearsOnlyFilter.gi() + Gear.TeethLimitGearFilter(min=10, max=20)
        actual = CombinationFinder.all_possible_combinations(gear_filter)
        self.assertEqual(expected, actual)

    def test_combinationfinder_all_combination_chains1(self):
        expected = [
            (0.0, {GearCombination(Gear12.gi(), Gear20.gi())}),
            (0.0, {GearCombination(Gear24.gi(), Gear40.gi())}),
            (0.0, {GearCombination(Gear36.gi(), TurntableGear60.gi())})
        ]
        actual = CombinationFinder.all_combination_chains(GearRatio.of_int_ratio(3, 5),
                                                          max_chain_length=1,
                                                          max_deviation=0.001)  # 0.1%
        self.compare_combinationfinder_result(expected, actual)

    def compare_combinationfinder_result(self, expected, actual):
        for ex, ac in zip(expected, actual):
            self.assertAlmostEqual(ex[0], ac[0])
            self.assertEqual(ex[1], ac[1])

    def test_combinationfinder_all_combination_chains2(self):
        expected = [
            (0.0051819, {GearCombination(WormGear.gi(), Gear8.gi()),
                         GearCombination(WormGear.gi(), Gear24.gi())}),
            (0.0051819, {GearCombination(WormGear.gi(), Gear12.gi()),
                         GearCombination(WormGear.gi(), Gear16.gi())})
        ]
        target_ratio = GearRatio.of_int_ratio(98, 18719)
        actual = CombinationFinder.all_combination_chains(target_ratio,
                                                          max_chain_length=2,
                                                          max_deviation=0.01)  # 1%
        self.compare_combinationfinder_result(expected, actual)

    def test_combinationfinder_all_combination_chains3(self):
        expected = [
            (0.01121463, {GearCombination(Gear8.gi(), Gear36.gi()),
                          GearCombination(WormGear.gi(), TurntableGear56.gi())}),
            (0.01121463, {GearCombination(Gear8.gi(), TurntableGear56.gi()),
                          GearCombination(WormGear.gi(), Gear36.gi())}),
            (0.02553602, {GearCombination(Gear12.gi(), TurntableGear56.gi()),
                          GearCombination(WormGear.gi(), TurntableGear56.gi())})
        ]
        target_ratio = GearRatio.of_int_ratio(23, 5861)
        actual = CombinationFinder.all_combination_chains(target_ratio,
                                                          max_chain_length=2,
                                                          max_deviation=0.03)  # 3%
        self.compare_combinationfinder_result(expected, actual)

    def test_combinationfinder_all_combination_chains4(self):
        expected = [(0.0142857, {GearCombination(Gear8.gi(), TurntableGear60.gi()),
                                 GearCombination(Gear12.gi(), TurntableGear56.gi())}),
                    (0.0142857, {GearCombination(Gear8.gi(), Gear24.gi()),
                                 GearCombination(Gear12.gi(), TurntableGear56.gi()),
                                 GearCombination(Gear24.gi(), TurntableGear60.gi())}),
                    (0.0142857, {GearCombination(Gear8.gi(), Gear40.gi()),
                                 GearCombination(Gear12.gi(), TurntableGear56.gi()),
                                 GearCombination(Gear40.gi(), TurntableGear60.gi())}),
                    (0.0142857, {GearCombination(Gear12.gi(), Gear36.gi()),
                                 GearCombination(Gear12.gi(), TurntableGear56.gi()),
                                 GearCombination(Gear24.gi(), TurntableGear60.gi())})]
        target_ratio = GearRatio.of_int_ratio(2, 71)
        actual = CombinationFinder.all_combination_chains(
            target_ratio,
            max_chain_length=3,
            max_deviation=0.03,
            combination_fltr=GearCombination.PossibleOnLiftbeamCombinationFilter())
        self.compare_combinationfinder_result(expected, actual)

    def test_combinationfinder_all_combination_chains5(self):
        self.maxDiff = None
        expected = results.COMBINATION_CHAINS_5
        target_ratio = GearRatio.of_int_ratio(23, 585861)
        actual = CombinationFinder.all_combination_chains(target_ratio,
                                                          max_chain_length=3,
                                                          max_deviation=0.03)  # 3%
        self.compare_combinationfinder_result(expected, actual)
