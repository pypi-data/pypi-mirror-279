from typing import *

from django.templatetags.static import static as dj_static

from .url_getters import URLGetter


__all__ = 'get_static', 'get_media',


def _url_getter(context, url_getter: Optional[URLGetter]):
    return url_getter if url_getter is not None else context.get('pdf_url_getter', None)


def get_static(
    path: str,
    context: dict = {},
    url_getter: Optional[URLGetter] = None,
):
    url_getter = _url_getter(context, url_getter)

    if url_getter is None:
        return dj_static(path)

    return url_getter.get_static(path)


def get_media(
    path: str,
    context: dict = {},
    url_getter: Optional[URLGetter] = None,
):
    url_getter = _url_getter(context, url_getter)

    if url_getter is None:
        return path

    return url_getter.get_media(path)
