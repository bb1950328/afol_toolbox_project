import abc
import importlib
import json
import os
from typing import List, Callable, Optional

from django.utils.safestring import mark_safe

import afol_toolbox_app
from afol_toolbox_app.view.menu import view

KEY_FILE_ICON = "file_icon"
KEY_MATERIALIZE_ICON = "materialize_icon"
KEY_DESCRIPTION = "description"
KEY_NAME = "name"
KEY_URL = "url"
KEY_CHILDREN = "children"
KEY_VIEW_FUNC = "view_func"


class MenuItem(abc.ABC):
    class Icon(abc.ABC):
        def as_html(self, size=2):
            """
            :param size: 0=1rem, 1=2rem, 2=4rem, 3=6rem
            :return: html code, already marked safe
            """
            if not 0 <= size <= 3:
                raise ValueError("size should be between 0 and 3 (see docstring)")
            return mark_safe(self._get_html_code(size))

        @abc.abstractmethod
        def _get_html_code(self, size):
            pass

    class MaterializeIcon(Icon):
        SIZE_CLASSES = ("tiny", "small", "medium", "large")

        def _get_html_code(self, size):
            size_class = self.SIZE_CLASSES[size]
            return f'<i class="{size_class} material-icons">{self._name}</i>'

        def __init__(self, name):
            self._name = name

        def __str__(self) -> str:
            return f"{self.__class__.__name__}[{self._name}]"

    class FileIcon(Icon):

        def _get_html_code(self, size):
            return f'<img src="{{% static "img/{self._path}" %}}" alt="Menu Icon" class="file-icon size{size}">'

        def __init__(self, path):
            self._path = path

        def __str__(self) -> str:
            return f"{self.__class__.__name__}[{self._path}]"

    class InexistentIcon(Icon):

        def _get_html_code(self, size):
            return ""

        def __str__(self) -> str:
            return "No icon"

    _name: str

    @property
    def name(self):
        return self._name

    _description: str

    @property
    def description(self):
        return self._description

    _icon: Icon

    @property
    def icon(self) -> Icon:
        return self._icon

    @property
    def parent(self):
        return self._parent

    _url: str

    @property
    def url(self) -> str:
        return self._url

    _absolute_url: str

    @property
    def absolute_url(self) -> str:
        return self._absolute_url

    def __init__(self, definition: dict, parent):
        self._name = definition[KEY_NAME]
        self._url = definition[KEY_URL]
        self._parent = parent

        if KEY_DESCRIPTION in definition:
            self._description = definition[KEY_DESCRIPTION]
        else:
            self._description = ""

        if KEY_MATERIALIZE_ICON in definition:
            self._icon = MenuItem.MaterializeIcon(definition[KEY_MATERIALIZE_ICON])
        elif KEY_FILE_ICON in definition:
            self._icon = MenuItem.FileIcon(definition[KEY_FILE_ICON])
        else:
            self._icon = MenuItem.InexistentIcon()

        parent_url = self.parent.absolute_url if self.parent else ""
        self._absolute_url = parent_url + "/" + self.url

    @staticmethod
    def of_definition(definition: dict, parent):
        if KEY_CHILDREN in definition:
            return Folder(definition, parent)
        else:
            return Tool(definition, parent)


class Folder(MenuItem):
    def __init__(self, definition: dict, parent):
        if KEY_CHILDREN not in definition:
            raise ValueError("the definition should have a children list!")
        super().__init__(definition, parent)
        self._children = [MenuItem.of_definition(de, self) for de in definition[KEY_CHILDREN]]

    @property
    def children(self) -> List[MenuItem]:
        return self._children


class Tool(MenuItem):
    _view_func: Callable

    @property
    def view_func(self) -> Callable:
        return self._view_func

    @staticmethod
    def _load_view_func(path: str) -> Callable:
        module_name, func_name = path.rsplit(".", 1)
        module_name = ".".join([afol_toolbox_app.__name__, view.__name__, module_name])
        print(module_name)
        module = importlib.import_module(module_name)
        func = getattr(module, func_name)
        return func

    def __init__(self, definition: dict, parent):
        if KEY_CHILDREN in definition:
            raise ValueError("the definition should not have a children list!")
        super().__init__(definition, parent)
        if KEY_VIEW_FUNC in definition:
            self._view_func = self._load_view_func(definition[KEY_VIEW_FUNC])
        else:
            self._view_func = lambda *args: ValueError("View function not defined")


def get_menudefinition_path() -> str:
    return os.path.join(os.path.dirname(__file__), "menudefiniton.json")


_menu: Optional[List[MenuItem]] = None


def get_menu() -> List[MenuItem]:  # todo convert to property
    global _menu
    if _menu is None:
        with open(get_menudefinition_path()) as _f:
            _menu = [MenuItem.of_definition(de, None) for de in json.load(_f)]
    return _menu


if __name__ == '__main__':
    """
    Prints the menu structure as tree
    """
    values = []
    col_widths = [1, 1, 1]


    def pr_tree(li: List[MenuItem], prefix=""):
        last = len(li) - 1
        original_prefix = prefix
        for i, elem in enumerate(li):
            prefix = original_prefix
            is_folder = isinstance(elem, Folder)
            is_last = i == last
            if is_last:
                prefix += "└─"
            else:
                prefix += "├─"
            if is_folder:
                prefix += "┬─"
            else:
                prefix += "──"
            values.append([elem, prefix + elem.name])
            if is_folder:
                new_prefix = original_prefix + ("│ " if not is_last else "  ")
                # noinspection PyUnresolvedReferences
                pr_tree(elem.children, new_prefix)


    pr_tree(get_menu())

    for ie in range(len(values)):
        row = values[ie]
        element = row[0]
        row.append(element.absolute_url)
        row.append(str(element.icon))

        for ic in range(len(col_widths)):
            cur_value = len(row[ic + 1])
            if cur_value > col_widths[ic]:
                col_widths[ic] = cur_value

    for ir, row in enumerate(values):
        for i_col in range(len(row) - 1):
            width = col_widths[i_col] + 2
            print(row[i_col + 1].ljust(width), end="")
        print()
