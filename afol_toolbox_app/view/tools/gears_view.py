# coding=utf-8
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render

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
