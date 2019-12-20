class MenuItem(object):
    _name: str

    @property
    def name(self):
        return self.name

    @name.setter
    def name(self, new_name):
        self._name = new_name

    _description: str

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, new_description):
        self.description = new_description

    _icon_name: str

    @property
    def icon_name(self):
        return self._icon_name

    @icon_name.setter
    def icon_name(self, new_icon_name):
        self._icon_name = new_icon_name

    def __init__(self, name, description, icon_name):
        self.name = name
        self.description = description
        self.icon_name = icon_name
