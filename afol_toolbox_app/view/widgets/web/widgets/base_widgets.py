# coding=utf-8
import abc
from collections import ItemsView
from typing import Optional, Dict

from afol_toolbox_app.model import util
from afol_toolbox_app.view.widgets.web import Listener, ClientListener, ServerListener


class BaseWidget(abc.ABC):
    class EventType(object):
        AFTER_PRINT = "onafterprint"
        BEFORE_PRINT = "onbeforeprint"
        BEFORE_UNLOAD = "onbeforeunload"
        HASH_CHANGE = "onhashchange"
        MESSAGE = "onmessage"
        OFFLINE = "onoffline"
        ONLINE = "ononline"
        PAGE_HIDE = "onpagehide"
        PAGE_SHOW = "onpageshow"
        POP_STATE = "onpopstate"
        STORAGE = "onstorage"
        UNLOAD = "onunload"
        ABORT = "onabort"
        AUTOCOMPLETE = "onautocomplete"
        AUTOCOMPLETE_ERROR = "onautocompleteerror"
        BLUR = "onblur"
        CANCEL = "oncancel"
        CAN_PLAY = "oncanplay"
        CAN_PLAY_THROUGH = "oncanplaythrough"
        CHANGE = "onchange"
        CLICK = "onclick"
        CLOSE = "onclose"
        CONTEXT_MENU = "oncontextmenu"
        CUE_CHANGE = "oncuechange"
        DBL_CLICK = "ondblclick"
        DRAG = "ondrag"
        DRAG_END = "ondragend"
        DRAG_ENTER = "ondragenter"
        DRAG_EXIT = "ondragexit"
        DRAG_LEAVE = "ondragleave"
        DRAG_OVER = "ondragover"
        DRAG_START = "ondragstart"
        DROP = "ondrop"
        DURATION_CHANGE = "ondurationchange"
        EMPTIED = "onemptied"
        ENDED = "onended"
        ERROR = "onerror"
        FOCUS = "onfocus"
        FOCUS_IN = "onfocusin"
        FOCUS_OUT = "onfocusout"
        INPUT = "oninput"
        INVALID = "oninvalid"
        KEY_DOWN = "onkeydown"
        KEY_PRESS = "onkeypress"
        KEY_UP = "onkeyup"
        LOAD = "onload"
        LOADED_DATA = "onloadeddata"
        LOADED_METADATA = "onloadedmetadata"
        LOAD_START = "onloadstart"
        MOUSE_DOWN = "onmousedown"
        MOUSE_ENTER = "onmouseenter"
        MOUSE_LEAVE = "onmouseleave"
        MOUSE_MOVE = "onmousemove"
        MOUSE_OUT = "onmouseout"
        MOUSE_OVER = "onmouseover"
        MOUSE_UP = "onmouseup"
        PAUSE = "onpause"
        PLAY = "onplay"
        PLAYING = "onplaying"
        PROGRESS = "onprogress"
        RATE_CHANGE = "onratechange"
        RESET = "onreset"
        RESIZE = "onresize"
        SCROLL = "onscroll"
        SEEKED = "onseeked"
        SEEKING = "onseeking"
        SELECT = "onselect"
        SORT = "onsort"
        STALLED = "onstalled"
        SUBMIT = "onsubmit"
        SUSPEND = "onsuspend"
        TIME_UPDATE = "ontimeupdate"
        TOGGLE = "ontoggle"
        VOLUME_CHANGE = "onvolumechange"
        WAITING = "onwaiting"
        WHEEL = "onwheel"
        ALL = [AFTER_PRINT, BEFORE_PRINT, BEFORE_UNLOAD, HASH_CHANGE, MESSAGE, OFFLINE, ONLINE, PAGE_HIDE, PAGE_SHOW,
               POP_STATE, STORAGE, UNLOAD, ABORT, AUTOCOMPLETE, AUTOCOMPLETE_ERROR, BLUR, CANCEL, CAN_PLAY,
               CAN_PLAY_THROUGH, CHANGE, CLICK, CLOSE, CONTEXT_MENU, CUE_CHANGE, DBL_CLICK, DRAG, DRAG_END, DRAG_ENTER,
               DRAG_EXIT, DRAG_LEAVE, DRAG_OVER, DRAG_START, DROP, DURATION_CHANGE, EMPTIED, ENDED, ERROR, FOCUS,
               FOCUS_IN, FOCUS_OUT, INPUT, INVALID, KEY_DOWN, KEY_PRESS, KEY_UP, LOAD, LOADED_DATA, LOADED_METADATA,
               LOAD_START, MOUSE_DOWN, MOUSE_ENTER, MOUSE_LEAVE, MOUSE_MOVE, MOUSE_OUT, MOUSE_OVER, MOUSE_UP, PAUSE,
               PLAY, PLAYING, PROGRESS, RATE_CHANGE, RESET, RESIZE, SCROLL, SEEKED, SEEKING, SELECT, SORT, STALLED,
               SUBMIT, SUSPEND, TIME_UPDATE, TOGGLE, VOLUME_CHANGE, WAITING, WHEEL, BEFORE_UNLOAD, HASH_CHANGE,
               MESSAGE, OFFLINE, ONLINE, PAGE_HIDE, PAGE_SHOW, POP_STATE, STORAGE, UNLOAD, ABORT, AUTOCOMPLETE,
               AUTOCOMPLETE_ERROR, BLUR, CANCEL, CAN_PLAY, CAN_PLAY_THROUGH, CHANGE, CLICK, CLOSE, CONTEXT_MENU,
               CUE_CHANGE, DBL_CLICK, DRAG, DRAG_END, DRAG_ENTER, DRAG_EXIT, DRAG_LEAVE, DRAG_OVER, DRAG_START, DROP,
               DURATION_CHANGE, EMPTIED, ENDED, ERROR, FOCUS, FOCUS_IN, FOCUS_OUT, INPUT, INVALID, KEY_DOWN, KEY_PRESS,
               KEY_UP, LOAD, LOADED_DATA, LOADED_METADATA, LOAD_START, MOUSE_DOWN, MOUSE_ENTER, MOUSE_LEAVE,
               MOUSE_MOVE, MOUSE_OUT, MOUSE_OVER, MOUSE_UP, PAUSE, PLAY, PLAYING, PROGRESS, RATE_CHANGE, RESET, RESIZE,
               SCROLL, SEEKED, SEEKING, SELECT, SORT, STALLED, SUBMIT, SUSPEND, TIME_UPDATE, TOGGLE, VOLUME_CHANGE,
               WAITING, WHEEL, ]

    class EventDict(object):
        _listeners: Dict[str, Listener]

        def __len__(self):
            return len(self._listeners)

        def __getitem__(self, item):
            return self._listeners[item]

        def __setitem__(self, key, value):
            if key not in BaseWidget.EventType.ALL:
                raise KeyError(f"key should be one of BaseWidget.EventType")
            if not isinstance(value, Listener):
                raise ValueError(f"Key should be a Listener, not {value.__class__}")
            self._listeners[key] = value
            # todo send change to client

        def __delitem__(self, key):
            del self._listeners[key]
            # todo send changes to client

        def __iter__(self):
            return self._listeners.__iter__()

        def __contains__(self, item):
            return self._listeners.__contains__(item)

        def items(self) -> ItemsView[str, Listener]:
            return self._listeners.items()

    def __init__(self, id=None):
        """
        :param id: optional, something like '3o0fq2zv4gaq' if not specified
        """
        self._id = util.get_random_alphanumeric_string(12) if id is None else id
        self._events = self.EventDict()

    @property
    def events(self) -> EventDict:
        return self._events

    @property
    def id(self):
        """
        :return: the id of the widget
        """
        return self._id

    @abc.abstractmethod
    def as_html(self) -> str:
        pass

    @property
    def joined_html_attributes(self) -> str:
        return " ".join((f'{key}="{value}"' for key, value in self.get_html_attributes().items()))

    def get_html_attributes(self) -> Dict[str, str]:
        listeners = {}
        for key, value in self.events.items():
            if isinstance(value, ClientListener):
                listeners[key] = value.js_code
            elif isinstance(value, ServerListener):
                listeners[key] = f'callServerListener("{self.id}", "{key}");'
            else:
                raise ValueError(f"Unsupported Listener class: {value.__class__}")
        return {**listeners, "id": self.id}


class SingleContainer(abc.ABC):
    """
    can contain zero or one child
    """
    _child: Optional[BaseWidget] = None

    @property
    def child(self) -> Optional[BaseWidget]:
        """
        :return: The child widget
        """
        return self._child

    @child.setter
    def child(self, child: BaseWidget):
        self._child = child
