# coding=utf-8
import abc


class BaseView(abc.ABC):
    @abc.abstractmethod
    def initialize(self):
        pass
