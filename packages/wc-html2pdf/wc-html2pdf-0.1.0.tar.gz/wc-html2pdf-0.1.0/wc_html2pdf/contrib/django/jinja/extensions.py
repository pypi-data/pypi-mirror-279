import jinja2
from jinja2.ext import Extension

from wc_html2pdf.contrib.django.shortcuts import get_static, get_media


__all__ = 'HTML2PDFUrlGetterExtension',


def _make_global(func):
    return jinja2.pass_context(lambda context, path, url_getter=None: func(
        path, context=context, url_getter=url_getter,
    ))


class HTML2PDFUrlGetterExtension(Extension):
    def __init__(self, environment):
        super().__init__(environment)
        environment.globals['html2pdf_static'] = _make_global(get_static)
        environment.globals['html2pdf_media'] = _make_global(get_media)
