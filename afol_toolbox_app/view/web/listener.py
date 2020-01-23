# coding=utf-8
import abc
import asyncio
from typing import Callable


class Listener(object, abc.ABC):
    pass


class ClientListener(Listener):
    def __init__(self, js_code):
        self._js_code = js_code

    @property
    def js_code(self) -> str:
        return self._js_code

    @js_code.setter
    def js_code(self, js_code) -> None:
        self._js_code = js_code


class ServerListener(Listener):
    def __init__(self, func: Callable):
        self._func = func

    @property
    def func(self) -> Callable:
        return self._func

    @func.setter
    def func(self, func: Callable) -> None:
        self._func = func


class AsyncServerListener(ServerListener):
    def __init__(self, async_func):
        self._async_func = async_func

    @property
    def func(self) -> Callable:
        return lambda: asyncio.run(self._async_func())

    @func.setter
    def func(self, async_func: Callable) -> None:
        self._async_func = async_func
