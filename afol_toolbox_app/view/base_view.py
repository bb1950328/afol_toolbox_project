# coding=utf-8
from typing import Any, Dict, List

from django.core.handlers.wsgi import WSGIRequest
from django.utils.safestring import mark_safe

from afol_toolbox_app.model.menu import menu_items


def render_menu(items: List[Any]) -> str:
    html = ""
    for mi in items:
        if isinstance(mi, menu_items.Folder):
            html += f'<div class="nav-folder">' \
                    f'<div class="nav-folder-label">{mi.name}</div>'
            html += render_menu(mi.children)
            html += "</div>"
        else:
            html += f'<div class="nav-leaf"><a href="{mi.absolute_url}" >{mi.name}</a></div>'
    return mark_safe(html)


def get_menu_context() -> Dict[str, Any]:
    return {
        "menu": render_menu(menu_items.get_menu()),
    }


def get_base_context(request: WSGIRequest) -> Dict[str, Any]:
    return {
        **get_menu_context()
    }