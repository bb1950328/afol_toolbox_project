# coding=utf-8
from afol_toolbox_app.model.gears import Gear8, Gear16, TurntableGear60, WormGear, GearCombination, \
    Gear12, Gear20, Gear28, TurntableGear28, TurntableGear56, Gear40, Gear24, Gear36

ALL_POSSIBLE_COMBINATIONS = [
    GearCombination(Gear8.gi(), Gear8.gi()),
    GearCombination(Gear8.gi(), Gear12.gi()),
    GearCombination(Gear8.gi(), Gear16.gi()),
    GearCombination(Gear8.gi(), Gear20.gi()),
    GearCombination(Gear8.gi(), Gear24.gi()),
    GearCombination(Gear8.gi(), Gear28.gi()),
    GearCombination(Gear8.gi(), Gear36.gi()),
    GearCombination(Gear8.gi(), Gear40.gi()),
    GearCombination(Gear8.gi(), TurntableGear28.gi()),
    GearCombination(Gear8.gi(), TurntableGear56.gi()),
    GearCombination(Gear8.gi(), TurntableGear60.gi()),
    GearCombination(Gear12.gi(), Gear8.gi()),
    GearCombination(Gear12.gi(), Gear12.gi()),
    GearCombination(Gear12.gi(), Gear16.gi()),
    GearCombination(Gear12.gi(), Gear20.gi()),
    GearCombination(Gear12.gi(), Gear24.gi()),
    GearCombination(Gear12.gi(), Gear28.gi()),
    GearCombination(Gear12.gi(), Gear36.gi()),
    GearCombination(Gear12.gi(), Gear40.gi()),
    GearCombination(Gear12.gi(), TurntableGear28.gi()),
    GearCombination(Gear12.gi(), TurntableGear56.gi()),
    GearCombination(Gear12.gi(), TurntableGear60.gi()),
    GearCombination(Gear16.gi(), Gear8.gi()),
    GearCombination(Gear16.gi(), Gear12.gi()),
    GearCombination(Gear16.gi(), Gear16.gi()),
    GearCombination(Gear16.gi(), Gear20.gi()),
    GearCombination(Gear16.gi(), Gear24.gi()),
    GearCombination(Gear16.gi(), Gear28.gi()),
    GearCombination(Gear16.gi(), Gear36.gi()),
    GearCombination(Gear16.gi(), Gear40.gi()),
    GearCombination(Gear16.gi(), TurntableGear28.gi()),
    GearCombination(Gear16.gi(), TurntableGear56.gi()),
    GearCombination(Gear16.gi(), TurntableGear60.gi()),
    GearCombination(Gear20.gi(), Gear8.gi()),
    GearCombination(Gear20.gi(), Gear12.gi()),
    GearCombination(Gear20.gi(), Gear16.gi()),
    GearCombination(Gear20.gi(), Gear20.gi()),
    GearCombination(Gear20.gi(), Gear24.gi()),
    GearCombination(Gear20.gi(), Gear28.gi()),
    GearCombination(Gear20.gi(), Gear36.gi()),
    GearCombination(Gear20.gi(), Gear40.gi()),
    GearCombination(Gear20.gi(), TurntableGear28.gi()),
    GearCombination(Gear20.gi(), TurntableGear56.gi()),
    GearCombination(Gear20.gi(), TurntableGear60.gi()),
    GearCombination(Gear24.gi(), Gear8.gi()),
    GearCombination(Gear24.gi(), Gear12.gi()),
    GearCombination(Gear24.gi(), Gear16.gi()),
    GearCombination(Gear24.gi(), Gear20.gi()),
    GearCombination(Gear24.gi(), Gear24.gi()),
    GearCombination(Gear24.gi(), Gear28.gi()),
    GearCombination(Gear24.gi(), Gear36.gi()),
    GearCombination(Gear24.gi(), Gear40.gi()),
    GearCombination(Gear24.gi(), TurntableGear28.gi()),
    GearCombination(Gear24.gi(), TurntableGear56.gi()),
    GearCombination(Gear24.gi(), TurntableGear60.gi()),
    GearCombination(Gear28.gi(), Gear8.gi()),
    GearCombination(Gear28.gi(), Gear12.gi()),
    GearCombination(Gear28.gi(), Gear16.gi()),
    GearCombination(Gear28.gi(), Gear20.gi()),
    GearCombination(Gear28.gi(), Gear24.gi()),
    GearCombination(Gear28.gi(), Gear28.gi()),
    GearCombination(Gear28.gi(), Gear36.gi()),
    GearCombination(Gear28.gi(), Gear40.gi()),
    GearCombination(Gear28.gi(), TurntableGear28.gi()),
    GearCombination(Gear28.gi(), TurntableGear56.gi()),
    GearCombination(Gear28.gi(), TurntableGear60.gi()),
    GearCombination(Gear36.gi(), Gear8.gi()),
    GearCombination(Gear36.gi(), Gear12.gi()),
    GearCombination(Gear36.gi(), Gear16.gi()),
    GearCombination(Gear36.gi(), Gear20.gi()),
    GearCombination(Gear36.gi(), Gear24.gi()),
    GearCombination(Gear36.gi(), Gear28.gi()),
    GearCombination(Gear36.gi(), Gear36.gi()),
    GearCombination(Gear36.gi(), Gear40.gi()),
    GearCombination(Gear36.gi(), TurntableGear28.gi()),
    GearCombination(Gear36.gi(), TurntableGear56.gi()),
    GearCombination(Gear36.gi(), TurntableGear60.gi()),
    GearCombination(Gear40.gi(), Gear8.gi()),
    GearCombination(Gear40.gi(), Gear12.gi()),
    GearCombination(Gear40.gi(), Gear16.gi()),
    GearCombination(Gear40.gi(), Gear20.gi()),
    GearCombination(Gear40.gi(), Gear24.gi()),
    GearCombination(Gear40.gi(), Gear28.gi()),
    GearCombination(Gear40.gi(), Gear36.gi()),
    GearCombination(Gear40.gi(), Gear40.gi()),
    GearCombination(Gear40.gi(), TurntableGear28.gi()),
    GearCombination(Gear40.gi(), TurntableGear56.gi()),
    GearCombination(Gear40.gi(), TurntableGear60.gi()),
    GearCombination(WormGear.gi(), Gear8.gi()),
    GearCombination(WormGear.gi(), Gear12.gi()),
    GearCombination(WormGear.gi(), Gear16.gi()),
    GearCombination(WormGear.gi(), Gear20.gi()),
    GearCombination(WormGear.gi(), Gear24.gi()),
    GearCombination(WormGear.gi(), Gear28.gi()),
    GearCombination(WormGear.gi(), Gear36.gi()),
    GearCombination(WormGear.gi(), Gear40.gi()),
    GearCombination(WormGear.gi(), TurntableGear28.gi()),
    GearCombination(WormGear.gi(), TurntableGear56.gi()),
    GearCombination(WormGear.gi(), TurntableGear60.gi()),
    GearCombination(TurntableGear28.gi(), Gear8.gi()),
    GearCombination(TurntableGear28.gi(), Gear12.gi()),
    GearCombination(TurntableGear28.gi(), Gear16.gi()),
    GearCombination(TurntableGear28.gi(), Gear20.gi()),
    GearCombination(TurntableGear28.gi(), Gear24.gi()),
    GearCombination(TurntableGear28.gi(), Gear28.gi()),
    GearCombination(TurntableGear28.gi(), Gear36.gi()),
    GearCombination(TurntableGear28.gi(), Gear40.gi()),
    GearCombination(TurntableGear28.gi(), TurntableGear28.gi()),
    GearCombination(TurntableGear28.gi(), TurntableGear56.gi()),
    GearCombination(TurntableGear28.gi(), TurntableGear60.gi()),
    GearCombination(TurntableGear56.gi(), Gear8.gi()),
    GearCombination(TurntableGear56.gi(), Gear12.gi()),
    GearCombination(TurntableGear56.gi(), Gear16.gi()),
    GearCombination(TurntableGear56.gi(), Gear20.gi()),
    GearCombination(TurntableGear56.gi(), Gear24.gi()),
    GearCombination(TurntableGear56.gi(), Gear28.gi()),
    GearCombination(TurntableGear56.gi(), Gear36.gi()),
    GearCombination(TurntableGear56.gi(), Gear40.gi()),
    GearCombination(TurntableGear56.gi(), TurntableGear28.gi()),
    GearCombination(TurntableGear56.gi(), TurntableGear56.gi()),
    GearCombination(TurntableGear56.gi(), TurntableGear60.gi()),
    GearCombination(TurntableGear60.gi(), Gear8.gi()),
    GearCombination(TurntableGear60.gi(), Gear12.gi()),
    GearCombination(TurntableGear60.gi(), Gear16.gi()),
    GearCombination(TurntableGear60.gi(), Gear20.gi()),
    GearCombination(TurntableGear60.gi(), Gear24.gi()),
    GearCombination(TurntableGear60.gi(), Gear28.gi()),
    GearCombination(TurntableGear60.gi(), Gear36.gi()),
    GearCombination(TurntableGear60.gi(), Gear40.gi()),
    GearCombination(TurntableGear60.gi(), TurntableGear28.gi()),
    GearCombination(TurntableGear60.gi(), TurntableGear56.gi()),
    GearCombination(TurntableGear60.gi(), TurntableGear60.gi()),
]

COMBINATION_CHAINS_4 = [
    {GearCombination(Gear8.gi(), TurntableGear60.gi()),
     GearCombination(WormGear.gi(), TurntableGear56.gi()),
     GearCombination(WormGear.gi(), TurntableGear60.gi())},

    {GearCombination(WormGear.gi(), Gear16.gi()),
     GearCombination(WormGear.gi(), Gear28.gi()),
     GearCombination(WormGear.gi(), TurntableGear56.gi())},

    {GearCombination(WormGear.gi(), Gear16.gi()),
     GearCombination(WormGear.gi(), TurntableGear28.gi()),
     GearCombination(WormGear.gi(), TurntableGear56.gi())},

    {GearCombination(WormGear.gi(), Gear12.gi()),
     GearCombination(WormGear.gi(), Gear36.gi()),
     GearCombination(WormGear.gi(), TurntableGear60.gi())}
]
