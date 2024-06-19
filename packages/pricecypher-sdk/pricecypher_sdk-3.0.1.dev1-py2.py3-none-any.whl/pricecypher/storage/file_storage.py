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
    _path_remote_base: str
    _path_remote_prefix: str

    def __init__(self, path_local: str, path_remote_base: str, path_remote_prefix: str):
        """
        :param path_local: Path on local filesystem where artifacts should be stored. We assume these artifacts are
            eventually uploaded to a remote location.
        :param path_remote_base: Base path of the remote storage, e.g. an URI pointing to the root of an S3 bucket.
        :param path_remote_prefix: Location within / on top of `path_remote_base` where remote artifacts will end up.

        NB: Values should be such that a locally stored 'file' at `path_local / file` matches with a remote copy at
        `path_remote_base / path_remote_prefix / file`.
        """
        self._path_local = path_local
        self._path_remote_base = path_remote_base
        self._path_remote_prefix = path_remote_prefix

    def get_path_local(self, filename: str) -> str:
        return os.path.join(self._path_local, filename)

    def get_path_remote(self, filename: str, full: bool = True) -> str:
        """
        :param filename: Name of the file.
        :param full: Whether the full remote path, so including `self._path_remote_base`, should be returned.
        :return: Path in remote storage. Either absolute (including 'base') or relative, depending on given `full`.
        """
        suffix = os.path.join(self._path_remote_prefix, filename)

        if not full:
            return suffix

        return os.path.join(self._path_remote_base, suffix)

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
        Open a file handler context to a new file in local storage.
        NB: the locally saved file should be uploaded to the remote storage automatically / externally.

        :param filename: Name of the file to save.
        :param mode: (Optional) Mimicks the `mode` parameter of the built-in `open` function. Defaults to 'w'.

        See Also
        --------
        - `Standard library reference <https://docs.python.org/3.7/library/functions.html#open>`__
        - `smart_open README.rst <https://github.com/RaRe-Technologies/smart_open/blob/master/README.rst>`__
        """
        if not self._path_local:
            raise InvalidStateException("The `path_local_outputs` and `path_local_outputs` must be set to save files.")

        local = self.get_path_local(filename)

        logging.info(f"Saving file, local path = '{local}', remote path = '{self.get_path_remote(filename)}'...")

        if self.get_scheme(local) == 'file':
            logging.debug("Making non-existing directories on the path to parent of `file_path_local`...")
            Path(local).parent.mkdir(parents=True, exist_ok=True)

        with smart_open.open(local, mode) as file:
            yield file

    @contextmanager
    def load(self, path: Union[Path, str], mode: str = 'r') -> str:
        """
        Open a file handler context to the give (remote) file path.

        :param path: Either an absolute path to a (remote) file, or a relative path from the remote file store.
        :param mode: (Optional) Mimicks the `mode` parameter of the built-in `open` function. Defaults to 'r'.
        """
        if isinstance(path, Path):
            path = path.as_posix()

        if self.get_scheme(path) == 'file' and not Path(path).is_absolute():
            path = self.get_path_remote(path)

        logging.debug(f"Loading / opening (remote) file at path '{path}'...")

        with smart_open.open(path, mode) as file:
            yield file

    @classmethod
    def from_handler_settings(cls: Type[FileStorage], settings: HandlerSettings) -> FileStorage:
        return cls(settings.path_local_out, settings.path_remote_out_base, settings.path_remote_out_prefix)
