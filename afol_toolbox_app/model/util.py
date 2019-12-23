# coding=utf-8


def get_class(object_or_class, min_base_class=object):
    if object_or_class.__class__ != type:
        object_or_class = object_or_class.__class__
    if not issubclass(object_or_class, min_base_class):
        raise ValueError(f"{object_or_class} isn't a subclass of {min_base_class} !")
    return object_or_class
