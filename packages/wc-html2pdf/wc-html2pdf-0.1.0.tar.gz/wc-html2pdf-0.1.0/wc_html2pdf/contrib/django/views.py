from typing import *
from functools import cached_property

from django.template.response import TemplateResponse
from django.views.generic.base import TemplateResponseMixin

from wc_html2pdf.converters import Converter
from .url_getters import URLGetter


class HTML2PDFTemplateResponse(TemplateResponse):
    def __init__(
        self,
        *args,
        converter: Converter,
        context: Optional[dict] = None,
        url_getter: Optional[URLGetter] = None,
        filename: Optional[str] = None,
        attachment: bool = True,
        **kwargs,
    ):
        self.converter = converter
        self.url_getter = url_getter

        super().__init__(*args, context=context, **kwargs)

        if filename:
            display = 'attachment' if attachment else 'inline'
            self['Content-Disposition'] = f'{display};filename="{filename}"'

    def resolve_context(self, context: Optional[dict]) -> dict:
        result_context = super().resolve_context(context)
        result_context = result_context if result_context is not None else {}
        result_context.setdefault('pdf_converter', self.converter)
        result_context.setdefault('pdf_url_getter', self.url_getter)

        return result_context

    @cached_property
    def source_content(self):
        return super().rendered_content

    @cached_property
    def rendered_content(self):
        content = self.source_content
        path = self.converter.from_content(content)

        with path.open('rb') as f:
            content = f.read()

        path.unlink()

        return content


class HTML2PDFTemplateResponseMixin(TemplateResponseMixin):
    response_class = HTML2PDFTemplateResponse
    content_type = 'application/pdf'

    pdf_converter: Optional[Converter] = None
    pdf_url_getter: Optional[URLGetter] = None
    pdf_filename: Optional[str] = None
    pdf_attachment: bool = True

    def get_pdf_filename(self) -> Optional[str]:
        return self.pdf_filename

    def get_pdf_url_getter(self) -> Optional[URLGetter]:
        return self.pdf_url_getter

    def get_pdf_converter(self) -> Converter:
        assert self.pdf_converter is not None, (
            'Either set `pdf_converter` attribute or change '
            '`get_pdf_converter` method to return `Converter` instance.'
        )

        return self.pdf_converter

    def render_to_response(self, context, **response_kwargs):
        response_kwargs.setdefault('attachment', self.pdf_attachment)
        response_kwargs.setdefault('filename', self.get_pdf_filename())
        response_kwargs.setdefault('converter', self.get_pdf_converter())
        response_kwargs.setdefault('url_getter', self.get_pdf_url_getter())

        return super().render_to_response(context, **response_kwargs)
