# coding=utf-8
import sys
from io import StringIO
from unittest import TestCase

from afol_toolbox_app.model.menu import menu_items
from afol_toolbox_app.view.tools.gears_view import data_table

md1 = {
    "name": "ABC",
    "description": "Description of ABC",
    "url": "abc",
    "materialize_icon": "abc_icon",
}

md2 = {
    "name": "XYZ",
    "url": "xyz",
    "file_icon": "/path/to/icon",
    "view_func": "tools.gears_view.data_table"
}

md3 = {
    "name": "XYZ",
    "url": "xyz",
    "children": [md1, md2],
}


class TestMenuItems(TestCase):
    def test_icon_as_html(self):
        ic = menu_items.MenuItem.MaterializeIcon("ac_unit")
        self.assertRaises(ValueError, lambda: ic.as_html(4))
        self.assertRaises(ValueError, lambda: ic.as_html(-1))

    def test_materialize_icon_str(self):
        ic = menu_items.MenuItem.MaterializeIcon("ac_unit")
        self.assertEqual("MaterializeIcon[ac_unit]", str(ic))

    def test_file_icon_str(self):
        ic = menu_items.MenuItem.FileIcon("abc.svg")
        self.assertEqual("FileIcon[abc.svg]", str(ic))

    def test_materialize_icon_html(self):
        ic = menu_items.MenuItem.MaterializeIcon("ac_unit")
        self.assertEqual('<i class="tiny material-icons">ac_unit</i>', ic.as_html(0))

    def test_file_icon_html(self):
        ic = menu_items.MenuItem.FileIcon("abc.svg")
        expected = '<img src="{% static "img/abc.svg" %}" alt="Menu Icon" class="file-icon size0" />'
        self.assertEqual(expected, ic.as_html(0))

    def test_inexistent_icon(self):
        ic = menu_items.MenuItem.InexistentIcon()
        self.assertEqual("", ic.as_html(2))
        self.assertTrue(str(ic))

    def test_definition_load(self):
        menu = menu_items.get_menu()
        for i in menu:
            self.assertIsInstance(i, menu_items.MenuItem)

    def test_item_1(self):
        i = menu_items.Tool(md1, None)
        self.assertEqual(md1["name"], i.name)
        self.assertEqual(md1["description"], i.description)
        self.assertEqual(md1["url"], i.url)
        self.assertEqual("/abc", i.absolute_url)
        self.assertIsNone(i.parent)
        self.assertEqual("MaterializeIcon[abc_icon]", str(i.icon))

    def test_item_2(self):
        parent = menu_items.Tool(md1, None)
        i = menu_items.Tool(md2, parent)
        self.assertEqual(md2["name"], i.name)
        self.assertEqual("", i.description)
        self.assertEqual(md2["url"], i.url)
        self.assertEqual("/abc/xyz", i.absolute_url)
        self.assertEqual(parent, i.parent)
        self.assertEqual("FileIcon[/path/to/icon]", str(i.icon))

    def test_item_3(self):
        i = menu_items.MenuItem.of_definition(md3, None)
        self.assertIsInstance(i.icon, menu_items.MenuItem.InexistentIcon)

    def test_tool_1(self):
        i = menu_items.Tool(md2, None)
        self.assertEqual(data_table, i.view_func)

    def test_tool_2(self):
        self.assertRaises(ValueError, lambda: menu_items.Tool(md3, None))  # should not have children

    def test_tool_3(self):
        i = menu_items.Tool(md1, None)
        func = i.view_func
        self.assertRaises(ValueError, lambda: func())  # no view function

    def test_tree_print(self):
        mi1 = menu_items.MenuItem.of_definition(md1, None)
        mi3 = menu_items.MenuItem.of_definition(md3, None)
        out_file = None
        old_stdout = None
        try:
            out_file = StringIO()
            old_stdout = sys.stdout
            sys.stdout = out_file
            menu_items.print_menudefinition_tree([mi1, mi3])
            output = out_file.getvalue()
            self.assertEqual("├───ABC    /abc      MaterializeIcon[abc_icon]  \n" +
                             "└─┬─XYZ    /xyz      No icon                    \n" +
                             "  ├───ABC  /xyz/abc  MaterializeIcon[abc_icon]  \n" +
                             "  └───XYZ  /xyz/xyz  FileIcon[/path/to/icon]    \n" +
                             "", output)
        finally:
            if old_stdout:
                sys.stdout = old_stdout
            if out_file:
                out_file.close()
