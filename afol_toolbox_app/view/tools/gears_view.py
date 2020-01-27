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
        data.append(["gears/" + gear.image_name, str(gear.teeth)+"T", str(gear.radius_in_mm)+" mm", gear.category])
    data.sort(key=lambda row: int(row[1][:-1]))
    context = {
        "table": show_as_table(
            ["Image", "Teeth", "Radius", "Category"],
            ["file_image", str, str, str],
            data
        ),
    }
    return render(request, "gear_table.html", context=context)
