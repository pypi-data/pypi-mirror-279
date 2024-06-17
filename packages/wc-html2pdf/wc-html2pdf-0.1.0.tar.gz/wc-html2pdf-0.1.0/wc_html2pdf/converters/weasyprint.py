from typing import *
from pathlib import Path
import tempfile

import weasyprint

from .base import Converter, PathType


__all__ = 'WeasyPrintConverter',


class WeasyPrintConverter(Converter):
    url_fetcher: Callable = staticmethod(weasyprint.default_url_fetcher)
    stylesheets: List[str] = []
    options: dict = {}

    def __init__(
        self,
        url_fetcher: Optional[Callable] = None,
        stylesheets: Optional[List[str]] = None,
        options: Optional[dict] = None,
    ):
        self.url_fetcher = url_fetcher if url_fetcher is not None else self.url_fetcher
        self.options = options if options is not None else self.options
        self.stylesheets = stylesheets if stylesheets is not None else self.stylesheets

    def get_font_config(self):
        return weasyprint.text.fonts.FontConfiguration()

    def get_stylesheets(self, stylesheets, base_url, url_fetcher, font_config):
        return [
            (
                value if not isinstance(value, str) else
                weasyprint.CSS(
                    value, base_url=base_url, url_fetcher=url_fetcher,
                    font_config=font_config,
                )
            )
            for value in stylesheets
        ]

    def _convert(
        self,
        *,
        content: Optional[str] = None,
        path: Optional[PathType] = None,
        file: Optional[IO] = None,
    ):
        assert content is not None or path is not None or file is not None, (
            'Either `content`, `path` or `file` parameters must be set to make conversion.'
        )

        url_fetcher = self.url_fetcher
        options = {**self.options}
        font_config = self.get_font_config()
        base_url = options.pop('base_url', None)
        stylesheets = list(options.pop('stylesheets', [])) + self.stylesheets

        html = weasyprint.HTML(
            string=content, filename=path, file_obj=file,
            base_url=base_url, url_fetcher=url_fetcher,
            **options,
        )
        options['stylesheets'] = self.get_stylesheets(
            stylesheets, base_url, url_fetcher, font_config,
        )
        document = html.render(font_config=font_config, **options)

        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as html_file:
            document.write_pdf(**options, target=html_file)

        return Path(html_file.name)

    def from_content(self, content: str):
        return self._convert(content=content)

    def from_file(
        self,
        *,
        path: Optional[PathType] = None,
        file: Optional[IO] = None,
    ):
        assert path is not None or file is not None, (
            'Either `path` or `file` parameters must be set to make conversion.'
        )
        assert path is None or file is None, (
            'Either `path` or `file` parameters must be set not both.'
        )
        return self._convert(path=path, file=file)
