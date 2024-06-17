from pathlib import Path
from django.apps import apps
from django.conf import settings as dj_settings


__all__ = (
    'URLGetter',
    'AbsoluteUrlGetter',
    'PathUrlGetter',
)


class URLGetter:
    def get_static(self, path: str) -> str:
        raise NotImplementedError()

    def get_media(self, path: str) -> str:
        raise NotImplementedError()


class AbsoluteUrlGetter(URLGetter):
    def __init__(self, url_prefix: str):
        self.url_prefix = url_prefix.rstrip('/') + '/'

    def get_static(self, path: str) -> str:
        if apps.is_installed('django.contrib.staticfiles'):
            from django.contrib.staticfiles.storage import staticfiles_storage

            path = staticfiles_storage.url(path)

        return self.url_prefix + path.lstrip('/')

    def get_media(self, path: str) -> str:
        return self.url_prefix + path.lstrip('/')


class PathUrlGetter(URLGetter):
    def format_file_path(self, path: str) -> str:
        return f'file://{path}'

    def get_static(self, path: str) -> str:
        if apps.is_installed('django.contrib.staticfiles'):
            from django.contrib.staticfiles.storage import staticfiles_storage

            return self.format_file_path(staticfiles_storage.path(path))

        return self.format_file_path(str(Path(dj_settings.STATIC_ROOT) / path))

    def get_media(self, path: str) -> str:
        if path.startswith(dj_settings.MEDIA_URL):
            path = path[len(dj_settings.MEDIA_URL):]

        return self.format_file_path(str(Path(dj_settings.MEDIA_ROOT) / path))
