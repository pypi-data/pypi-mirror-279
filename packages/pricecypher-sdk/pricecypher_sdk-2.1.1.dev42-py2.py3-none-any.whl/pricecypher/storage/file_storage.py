from __future__ import annotations

import logging
import os
import re
from abc import ABC
from contextlib import contextmanager
from pathlib import Path
from typing import Type, Union

import smart_open

from pricecypher.dataclasses import HandlerSettings
from pricecypher.exceptions import InvalidStateException

p_has_url_proto = re.compile('(.+)://(.+)')


class FileStorage(ABC):
    _path_local: str
    _path_remote: str

    def __init__(self, path_local: str, path_remote: str):
        self._path_local = path_local
        self._path_remote = path_remote

    def get_path_local(self, filename: str) -> str:
        return os.path.join(self._path_local, filename)

    def get_path_remote(self, filename: str) -> str:
        return os.path.join(self._path_remote, filename)

    @classmethod
    def get_scheme(cls, uri_as_string):
        uri = smart_open.parse_uri(uri_as_string)
        return uri.scheme if hasattr(uri, 'scheme') else None

    def get_scheme_local(self, filename: str) -> str:
        return self.get_scheme(self.get_path_local(filename))

    def get_scheme_remote(self, filename: str) -> str:
        return self.get_scheme(self.get_path_remote(filename))

    @contextmanager
    def save(self, filename: str, mode: str = 'w') -> str:
        """
        TODO

        :param filename: Name of the file to save.
        :param mode: (Optional) Mimicks the `mode` parameter of the built-in `open` function.
        :: A file-like object. - See also __

        See Also
        --------
        - `Standard library reference <https://docs.python.org/3.7/library/functions.html#open>`__
        - `smart_open README.rst <https://github.com/RaRe-Technologies/smart_open/blob/master/README.rst>`__
        """
        if not self._path_local or not self._path_remote:
            raise InvalidStateException("The `path_local_outputs` and `path_local_outputs` must be set to save files.")

        local = self.get_path_local(filename)
        remote = self.get_path_remote(filename)

        logging.info(f"Saving file, local path = '{local}', remote path = '{remote}'...")

        if self.get_scheme(local) == 'file':
            logging.debug("Making non-existing directories on the path to parent of `file_path_local`...")
            Path(local).parent.mkdir(parents=True, exist_ok=True)

        with smart_open.open(local, mode) as file:
            yield file

    @contextmanager
    def load(self, path: Union[Path, str], mode: str = 'r') -> str:
        if isinstance(path, Path):
            path = path.as_posix()

        if self.get_scheme(path) == 'file' and not Path(path).is_absolute():
            path = self.get_path_remote(path)

        print(f"opening {path}...")

        with smart_open.open(path, mode) as file:
            yield file

    @classmethod
    def from_handler_settings(cls: Type[FileStorage], settings: HandlerSettings) -> FileStorage:
        return cls(settings.path_local_outputs, settings.path_remote_outputs)
