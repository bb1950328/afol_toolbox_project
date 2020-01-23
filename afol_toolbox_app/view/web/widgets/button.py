# coding=utf-8
from afol_toolbox_app.view.web.widgets.base_widgets import BaseWidget, SingleContainer


class Button(BaseWidget, SingleContainer):
    def as_html(self) -> str:
        child_html = self.child.as_html() if self.child else ""
        return f'<button id="{self.id}">{child_html}</button>'
