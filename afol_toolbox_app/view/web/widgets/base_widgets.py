# coding=utf-8
import abc

from afol_toolbox_app.model import util


class BaseWidget(abc.ABC):

    def __init__(self):
        self._id = util.get_random_alphanumeric_string(12)

    @property
    def id(self):
        """
        :return: the id of the widget, something like '3o0fq2zv4gaq'
        """
        return self._id

    @abc.abstractmethod
    def as_html(self) -> str:
        pass
