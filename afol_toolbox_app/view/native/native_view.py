# coding=utf-8
from kivy.app import App
from kivy.uix.button import Button

from afol_toolbox_app.view.base.base_view import BaseView
import kivy

kivy.require('1.0.1')


class AfolApp(App):

    def build(self):
        app = super().build()
        button = Button()
        button.text = "Click me!"
        app.add_widget(button)
        return app


class NativeView(BaseView):
    def initialize(self):
        pass


if __name__ == '__main__':
    AfolApp().run()
