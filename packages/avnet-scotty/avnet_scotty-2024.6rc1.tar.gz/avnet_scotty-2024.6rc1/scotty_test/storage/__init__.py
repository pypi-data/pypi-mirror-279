# SPDX-FileCopyrightText: (C) 2023 Avnet Embedded GmbH
# SPDX-License-Identifier: GPL-3.0-only
"""Azure storage functions for scotty-test."""

import os
import logging
from typing import List, Set

from azure.storage.blob import ContainerClient


class StorageClient():
    """Azure storage client."""

    def __init__(self, token: str, *args, **kwargs):
        """Construct the client."""
        self.__token = token
        self.__container = ContainerClient.from_connection_string(
            conn_str=self.__token,
            container_name='blob-sync'
        )

    def local_storage(self) -> str:
        """Return the path to the local storage."""
        return os.path.join(os.environ.get('HOME', '/tmp'), '.local', 'scotty-test')

    def _get_fromlocal_storage(self, path, hash) -> str:
        needle = f'{self.local_storage()}/{path}.{hash}'
        if os.path.exists(needle):
            return needle
        return None

    def _put_tolocal_storage(self, path, hash, stream) -> str:
        needle = f'{self.local_storage()}/{path}.{hash}'
        os.makedirs(os.path.dirname(needle), exist_ok=True)
        with open(needle, 'wb') as o:
            o.write(stream)
        return needle

    def blob_list(self, path) -> List[object]:
        """List blob info."""
        return [x for x in self.__container.list_blobs(name_starts_with=path.lstrip('/') if path else None)]

    def list(self, path: str) -> List[str]:
        """List blob names."""
        return [x.name for x in self.blob_list(path)]

    def list_dirs(self, path: str) -> Set[str]:
        """List directories in the blob storage."""
        return {x.split('/')[0] for x in self.list(path) if '/' in x}

    def download(self, path: str) -> str:
        """Download a blob."""
        expected_hash = self.blob_hash(path)
        res = self._get_fromlocal_storage(path, expected_hash)
        if res is not None:
            return res
        logging.getLogger(
            'scotty-test').info(f'Downloading {path}, please wait...')
        return self._put_tolocal_storage(path,
                                         expected_hash,
                                         self.__container.download_blob(path.lstrip('/')).readall())

    def blob_hash(self, path: str) -> str:
        """Hash of the content of a blob."""
        try:
            return self.blob_list(path)[0].content_settings.content_md5.hex()
        except (IndexError, AttributeError):
            return ''
