# coding=utf-8
import json
from unittest import TestCase

from afol_toolbox_app.model.menu import menu_items


class TestMenuDefinition(TestCase):
    def check_menudefinition_list(self, md_list):
        self.assertEqual(list, type(md_list))
        urls = []
        for md_dict in md_list:
            self.check_menudefinition(md_dict)
            urls.append(md_dict[menu_items.KEY_URL])
        for u in urls:
            self.assertEqual(1, urls.count(u), f"the url attribute should be unique within the same parent! "
                                               f"('{u}' is not)")

    def check_menudefinition(self, md_dict):
        self.assertEqual(dict, type(md_dict))
        self.assertTrue(menu_items.KEY_NAME in md_dict)
        self.assertTrue(menu_items.KEY_URL in md_dict)
        if menu_items.KEY_MATERIALIZE_ICON not in md_dict and menu_items.KEY_FILE_ICON not in md_dict:
            print(f"WARNING: '{md_dict['name']}' has no icon!")
        if menu_items.KEY_CHILDREN in md_dict:
            self.check_menudefinition_list(md_dict[menu_items.KEY_CHILDREN])
        else:
            self.assertTrue(menu_items.KEY_VIEW_FUNC in md_dict)

    def test_menudefinition_format(self):
        with open(menu_items.get_menudefinition_path()) as f:
            md = json.load(f)
        self.check_menudefinition_list(md)
