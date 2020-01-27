# coding=utf-8
from django.shortcuts import render
from django.template import defaulttags
from django.utils.safestring import mark_safe


def show_as_table(request, heads, types, data) -> dict:
    context = {
        "heads": heads,
        "rows": []
    }
    for row in data:
        res = []
        for i_col, value in enumerate(row):
            dtype = types[i_col]
            if dtype == bool:
                res.append(mark_safe(
                    f'<i class="material-icons" style="color: {"green" if value else "red"}">'
                    f'{"tick" if value else "cross"}</i>'  # todo lookup correct icon names
                ))
            elif dtype == "file_image":
                res.append(mark_safe(
                    f'<img alt="{value}" src="/static/img/1mp/{value}" />'
                ))
            # todo add more types...
            else:
                res.append(str(value))
        context["rows"].append(res)

    http_response = render(request, "table.html", context=context)
    return mark_safe(http_response.content.decode())
