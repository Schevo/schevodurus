"""Durus backend."""

# Copyright (c) 2001-2009 ElevenCraft Inc.
# See LICENSE for details.

import os
import sys

# Set Durus logging level before importing rest of Durus.
from durus.logger import logger
from logging import ERROR
logger.setLevel(ERROR)

from durus.btree import BTree
from durus.connection import Connection
from durus.file_storage import FileStorage
from durus.persistent_dict import PersistentDict
from durus.persistent_list import PersistentList

from schevo.error import DatabaseFileLocked

from schevodurus.backend_test_classes import (
    TestMethods_CreatesDatabase,
    TestMethods_CreatesSchema,
    TestMethods_EvolvesSchemata,
    )

if sys.platform == 'win32':
    import pywintypes
    FileLockedError = pywintypes.error
else:
    FileLockedError = IOError


DEFAULT_CACHE_SIZE = 100000


class DurusBackend(object):

    description = 'Backend that directly uses Durus 3.8'
    backend_args_help = """
    cache_size=SIZE
        Set the size of the in-memory object cache to SIZE, which is an
        integer specifying the maximum number of objects to keep in the
        cache.
    """

    __test__ = False

    BTree = BTree
    PDict = PersistentDict
    PList = PersistentList

    TestMethods_CreatesDatabase = TestMethods_CreatesDatabase
    TestMethods_CreatesSchema = TestMethods_CreatesSchema
    TestMethods_EvolvesSchemata = TestMethods_EvolvesSchemata

    def __init__(self, filename, cache_size=DEFAULT_CACHE_SIZE):
        """Create a new `DurussBackend` instance.

        - `filename`: Name of file to open with this backend.
        - `cache_size`: Maximum number of objects to keep in the
          in-memory object cache.
        """
        self._filename = filename
        self._cache_size = cache_size
        self._is_open = False
        self.open()

    @classmethod
    def args_from_string(cls, s):
        """Return a dictionary of keyword arguments based on a string given
        to a command-line tool."""
        kw = {}
        if s is not None:
            for arg in (p.strip() for p in s.split(',')):
                name, value = (p2.strip() for p2 in arg.split('='))
                if name == 'cache_size':
                    kw[name] = int(value)
                elif name == 'storage':
                    kw[name] = value
                else:
                    raise KeyError(
                        '%s is not a valid name for backend args' % name)
        return kw

    @classmethod
    def usable_by_backend(cls, filename):
        """Return (`True`, *additional backend args*) if the named
        file is usable by this backend, or `False` if not."""
        # Get first 128 bytes of file.
        f = open(filename, 'rb')
        try:
            try:
                header = f.read(128)
            except IOError:
                if sys.platform == 'win32':
                    raise DatabaseFileLocked()
                else:
                    raise
        finally:
            f.close()
        # Look for Durus shelf storage signature and
        # durus module signature.
        if 'durus.persistent_dict' in header:
            if header[:7] == 'SHELF-1':
                return (True, {})
        return False

    @property
    def has_db(self):
        """Return `True` if the backend contains a Schevo database."""
        return self.get_root().has_key('SCHEVO')

    def close(self):
        """Close the underlying storage (and the connection if
        needed)."""
        self.storage.close()
        self._is_open = False

    def commit(self):
        """Commit the current transaction."""
        self.conn.commit()

    def get_root(self):
        """Return the backend's `root` object."""
        return self.conn.get_root()

    def open(self):
        """Open the underlying storage based on initial arguments."""
        if not self._is_open:
            self.storage = FileStorage(self._filename)
            try:
                self.storage.shelf.file.obtain_lock()
            except FileLockedError, e:
                raise DatabaseFileLocked()
            self.conn = Connection(self.storage, cache_size=self._cache_size)
            self._is_open = True

    def pack(self):
        """Pack the underlying storage."""
        self.conn.pack()

    def rollback(self):
        """Abort the current transaction."""
        self.conn.abort()
