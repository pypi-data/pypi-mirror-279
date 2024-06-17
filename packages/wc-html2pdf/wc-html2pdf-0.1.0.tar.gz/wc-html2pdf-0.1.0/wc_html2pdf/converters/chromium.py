from typing import *
from pathlib import Path
import subprocess
import tempfile

from .base import Converter, PathType


__all__ = 'ChromiumConverter',


class ChromiumConverter(Converter):
    bin_path: PathType = '/usr/bin/chromium'
    options: List[str] = [
        '--disable-gpu',
        '--no-margins',
        '--run-all-compositor-stages-before-draw',
        '--disable-crash-reporter',
        '--disable-extensions',
        '--disable-popup-blocking',
        '--disable-checker-imaging',
        '--no-pdf-header-footer',
        '--disable-pdf-tagging',
        '--no-sandbox',
        '--virtual-time-budget=1000',
    ]

    def __init__(
        self,
        bin_path: Optional[PathType] = None,
        options: Optional[List[str]] = None,
    ):
        bin_path = bin_path if bin_path is not None else self.bin_path

        assert isinstance(self.bin_path, (str, Path)) and self.bin_path != '', (
            'Path to a executable(bin_path) must not be empty.'
        )

        self.bin_path = bin_path
        self.options = options if options is not None else self.options

    def from_content(self, content: str):
        with tempfile.NamedTemporaryFile(suffix='.html') as html_file:
            html_file.write(str.encode(content))
            html_file.flush()

            return self.from_file(path=html_file.name)

    def from_file(
        self,
        *,
        path: Optional[PathType] = None,
        file: Optional[IO] = None,
    ):
        assert path is not None or file is not None, (
            'Either `path` or `file` parameters must be set to make conversion.'
        )

        if file is not None:
            path = file.name

        pdf_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        pdf_file.close()
        input_url = 'file://{0}'.format(str(path))

        self.run_conversion(self.bin_path, input_url, pdf_file.name, self.options)

        return Path(pdf_file.name)

    def run_conversion(
        self,
        bin_path: PathType,
        input_url: str,
        output_path: PathType,
        options: List[str],
    ):
        command = [f'{bin_path}', '--headless'] + options + [
            f'--print-to-pdf={output_path}',
            f'{input_url}',
        ]
        subprocess.run(command, check=True, capture_output=True)
