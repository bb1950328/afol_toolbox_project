# coding=utf-8
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render

from afol_toolbox_app.model import gears
from afol_toolbox_app.view.table_view import show_as_table


def data_table(request: WSGIRequest) -> HttpResponse:
    data = []
    for gear in gears.Gear.get_all():
        gear = gear.gi()
        data.append(["gears/" + gear.image_name, gear.teeth, str(gear.radius_in_mm)+" mm"])
    data.sort(key=lambda row: row[1])
    context = {
        "table": show_as_table(
            request,
            ["Image", "Teeth", "Radius"],
            ["file_image", int, int],
            data
        ),
    }
    return render(request, "gear_table.html", context=context)
