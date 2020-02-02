# coding=utf-8
import json

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.safestring import mark_safe

from afol_toolbox_app.model import gears
from afol_toolbox_app.view.base_view import get_base_context
from afol_toolbox_app.view.table_view import show_as_table_client


def data_table(request: WSGIRequest) -> HttpResponse:
    data = []
    for gear in gears.Gear.get_all():
        gear = gear.gi()
        data.append(["gears/" + gear.image_name, gear.teeth, gear.radius_in_mm, gear.category])
    data.sort(key=lambda row: row[1])
    context = {
        "table": show_as_table_client(
            ["Image", "Teeth", "Radius", "Category"],
            ["file_image", "number", "number", "str"],
            [None, "T", " mm", None],
            data
        ),
        **get_base_context(request),
    }
    return render(request, "gear_table.html", context=context)


def ratio_calculator(request: WSGIRequest) -> HttpResponse:
    gears_data = []
    groups = []
    for group, glist in (("Worm Gears", gears.WormGear.get_all()),
                         ("Gears", gears.NormalGear.get_all()),
                         ("Turntables", gears.TurntableGear.get_all())):
        gr_data = []
        for g in glist:
            g = g.gi()
            gr_data.append({"name": g.display_name, "teeth": g.teeth})
        gears_data.append(gr_data)
        groups.append(group)
    context = {
        **get_base_context(request),
        "gears_data": mark_safe(json.dumps(gears_data)),
        "gear_groups": mark_safe(json.dumps(groups)),
    }
    return render(request, "ratio_calculator.html", context)


def ratio_finder(request: WSGIRequest) -> HttpResponse:
    post = {"csrfmiddlewaretoken": "Dd5W1ToBlgGB0U7BO1t0CopCggOhgqJYjViRye55e4kYOkDEqpZdj8mQyPCSSnYS",
            "select_ratio_format": "a_b", "input_a": "1", "input_b": "1", "select_max_gears": "2", "max_results": "19",
            "check_no_worm": "on", "combination_ratio_min": "1", "combination_ratio_max": "100"}
    context = {
        **get_base_context(request),
    }
    if len(post):  # todo clear post after
        input_a = float(post["input_a"])
        input_b = float(post["input_b"])
        max_combinations = int(post["select_max_gears"]) // 2
        max_results = int(float(post["max_results"]))
        max_deviation = float(post["max_deviation"])
        no_worm = post["check_no_worm"] == "on"
        no_turntables = post["check_no_turntables"] == "on"
        combi_ratio_min = int(post["combination_ratio_min"])
        combi_ratio_max = int(post["combination_ratio_max"])
        ratio = gears.GearRatio.of_ratio(input_a, input_b)
        ratio_filter = gears.Gear.AllGearsFilter.gi()
        combi_filter = gears.GearCombination.AllGearCombinationsFilter.gi()
        result = gears.CombinationFinder.all_combination_chains(ratio=ratio,
                                                                max_results=max_results,
                                                                max_chain_length=max_combinations,
                                                                max_deviation=max_deviation,
                                                                ratio_filter=ratio_filter,
                                                                combination_fltr=combi_filter)
        context["result_table"] = show_as_table_client(
            heads=["Deviation", ],
            types=["number", ],
            units=["%", ],
            data=result,
        )
    return render(request, "ratio_finder.html", context)
