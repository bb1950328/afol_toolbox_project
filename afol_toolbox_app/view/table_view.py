# coding=utf-8
from django.utils.safestring import mark_safe


def show_as_table(heads, types, data, group_same=True, bigger_on_hover=True) -> dict:
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
                       f'{"tick" if value else "cross"}</i>'  # todo lookup correct icon names

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
