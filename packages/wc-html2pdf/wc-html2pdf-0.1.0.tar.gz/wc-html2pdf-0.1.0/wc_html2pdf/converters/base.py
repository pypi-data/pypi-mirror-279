from typing import *
from pathlib import Path


__all__ = 'Converter',

PathType = Union[str, Path]


class Converter:
    def from_content(self, content: str) -> Path:
        raise NotImplementedError()

    def from_file(
        self,
        *,
        path: Optional[Union[str, Path]] = None,
        file: Optional[IO] = None,
    ) -> Path:
        raise NotImplementedError()
