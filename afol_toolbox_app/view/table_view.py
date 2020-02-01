# coding=utf-8
from typing import Any
from typing import List
from typing import Optional

from django.core.handlers.wsgi import WSGIRequest
from django.utils.safestring import mark_safe
import json

ICON_FALSE = "clear"
ICON_TRUE = "check"


def show_as_table_server(request: WSGIRequest,
                         heads, types, data,
                         group_same=True, bigger_on_hover=True,
                         sort=None) -> dict:
    sort = request.GET.get("sort", sort)
    table = "<table><thead><tr>"
    for h in heads:
        table += f"\n<th>{h}</th>"
    table += "\n</tr></thead>\n<tbody>"

    cells = []
    for row in data:
        cells.append([])
        for i_col, value in enumerate(row):
            dtype = types[i_col]
            if dtype == bool:
                cell = f'<i class="material-icons" style="color: {"green" if value else "red"}">' \
                       f'{ICON_TRUE if value else ICON_FALSE}</i>'

            elif dtype == "file_image":
                cell = f'<img alt="{value}" src="/static/img/1mp/{value}" />'
            # todo add more types...
            else:
                cell = str(value)
            cells[-1].append(cell)

    num_rows = len(cells)
    num_cols = len(cells[0])

    for i_row, row in enumerate(data):
        table += f'\n<tr id="tr{i_row}">'
        for i_col, value in enumerate(row):
            cell = cells[i_row][i_col]
            if cell is not None:
                rowspan = 1
                colspan = 1
                if group_same:
                    ir = i_row + 1
                    ic = i_col
                    while ir < num_rows and cells[ir][ic] == cell:
                        cells[ir][ic] = None
                        rowspan += 1
                        ir += 1
                    if rowspan == 1:  # cant use both rowspan and colspan
                        ic += 1
                        ir -= 1
                        while ic < num_cols and cells[ir][ic] == cell:
                            cells[ir][ic] = None
                            colspan += 1
                            ic += 1
                cls = "bigger-on-hover" if bigger_on_hover else ""
                table += f'\n<td id="td{i_row}_{i_col}" ' \
                         f'rowspan="{rowspan}" colspan="{colspan}" ' \
                         f'class="{cls}">{cell}</td>'
        table += "\n</tr>"
    table += "\n</tbody></table>"
    return mark_safe(table)


@mark_safe
def show_as_table_client(heads: List[str],
                         types: List[str],
                         units: List[Optional[str]],
                         data: List[List[Any]],
                         sorted_column=None) -> str:
    sort_states = [0] * len(heads)  # 0=none, 1=asc, 2=desc
    if not sorted_column:
        if "number" in types:
            sorted_column = types.index("number")
        elif "str" in types:
            sorted_column = types.index("str")
        else:
            sorted_column = 0
    sort_states[sorted_column] = 1
    html = '<table id="at_table">\n<thead id="at_thead"></thead>\n<tbody id="at_tbody"></tbody>\n</table>\n<script>\n'
    html += f'const heads = {json.dumps(heads)};\n'
    html += f'const types = {json.dumps(types)};\n'
    html += f'const value_units = {json.dumps(units)};\n'
    html += f'var sort_states = {json.dumps(sort_states)};\n'
    html += f'var cells = {json.dumps(data)};\n'
    html += "render_table();"
    html += "</script>"
    return html
