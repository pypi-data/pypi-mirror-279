from typing import *

from django import template
from wc_html2pdf.contrib.django.url_getters import URLGetter
from wc_html2pdf.contrib.django.shortcuts import get_static, get_media


register = template.Library()


@register.simple_tag(takes_context=True)
def html2pdf_static(
    context,
    path: str,
    url_getter: Optional[URLGetter] = None,
):
    return get_static(path, context=context, url_getter=url_getter)


@register.simple_tag(takes_context=True)
def html2pdf_media(
    context,
    path: str,
    url_getter: Optional[URLGetter] = None,
):
    return get_media(path, context=context, url_getter=url_getter)
