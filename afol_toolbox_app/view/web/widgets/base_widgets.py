# coding=utf-8
import abc
from typing import Optional

from afol_toolbox_app.model import util


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
