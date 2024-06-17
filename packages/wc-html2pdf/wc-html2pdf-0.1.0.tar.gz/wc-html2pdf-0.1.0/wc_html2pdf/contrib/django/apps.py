from django.apps import AppConfig
from django.utils.translation import pgettext_lazy


__all__ = 'HTML2PDFConfig',


class HTML2PDFConfig(AppConfig):
    name = 'wc_html2pdf.contrib.django'
    label = 'wc_html2pdf_django'
    verbose_name = pgettext_lazy('wc_html2pdf', 'HTML 2 PDF')
