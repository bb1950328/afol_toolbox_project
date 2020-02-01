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
    context = {
        **get_base_context(request),
    }
    return render(request, "ratio_finder.html", context)
