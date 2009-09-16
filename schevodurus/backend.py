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
from durus.error import ConflictError
from durus.file_storage import FileStorage
from durus.persistent_dict import PersistentDict
from durus.persistent_list import PersistentList

import duruses.client

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


class DurusBackend(object):
    """Schevo backend that directly uses Durus 3.9.

    NOTE: A Durus connection should be used by a process or thread for
    only one Schevo database instance, and should not be used for
    other purposes.  Create a new Durus connection instance for each
    Schevo database instance.
    """

    DEFAULT_CACHE_SIZE = 100000
    DEFAULT_DURUSES_PORT = duruses.client.DEFAULT_PORT

    description = __doc__.splitlines()[0].strip()
    backend_args_help = """
    Common options:

        readonly=False (bool)
            Whether or not to use database in readonly mode.

    Options for using single-process files on disk:

        cache_size=%(DEFAULT_CACHE_SIZE)i (int)
            Maximum number of objects to keep in the cache.

    Options for using a pre-existing Durus storage instance:
    Filename is ignored when Durus options are used.

        durus_storage=None (durus.storage.Storage instance)
            An existing Durus storage instance to use.

    Options for using a Duruses server:
    Filename is ignored when duruses options are used.

        duruses_db_name=None (str)
            Name of the Duruses database to use.

        duruses_host=None (str)
            Host name of the Duruses server to connect to.
            Combined with duruses_port, creates a new client connection.

        duruses_port=%(DEFAULT_DURUSES_PORT)i (int)
            Port of the Duruses server to connect to.

        duruses_client=None (duruses.client.Client instance)
            An existing client connection to use.
    """ % locals()

    __test__ = False

    BTree = BTree
    PDict = PersistentDict
    PList = PersistentList

    conflict_exceptions = (ConflictError,)

    TestMethods_CreatesDatabase = TestMethods_CreatesDatabase
    TestMethods_CreatesSchema = TestMethods_CreatesSchema
    TestMethods_EvolvesSchemata = TestMethods_EvolvesSchemata

    def __init__(self, filename,
                 readonly=False,
                 cache_size=DEFAULT_CACHE_SIZE,
                 durus_storage=None,
                 duruses_db_name=None,
                 duruses_host=None, duruses_port=DEFAULT_DURUSES_PORT,
                 duruses_client=None):
        """Create a new `DurusBackend` instance"""
        self._filename = filename
        self._readonly = readonly
        self._cache_size = cache_size
        self._durus_storage = durus_storage
        self._duruses_db_name = duruses_db_name
        self._duruses_host = duruses_host
        self._duruses_port = duruses_port
        self._duruses_client = duruses_client
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
                elif name == 'duruses_host':
                    kw[name] = value
                elif name == 'duruses_port':
                    kw[name] = int(value)
                elif name == 'duruses_db_name':
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
            # Find or create storage.
            if self._durus_storage is not None:
                self.storage = self._durus_storage
            elif None not in (self._duruses_host, self._duruses_port,
                              self._duruses_db_name):
                self._duruses_client = duruses.client.Client(
                    self._duruses_host, self._duruses_port)
                self.storage = self._duruses_client.storage(
                    self._duruses_db_name)
            elif None not in (self._duruses_client, self._duruses_db_name):
                self.storage = self._duruses_client.storage(
                    self._duruses_db_name)
            else:
                try:
                    self.storage = FileStorage(self._filename)
                    self.storage.shelf.file.obtain_lock()
                except FileLockedError, e:
                    raise DatabaseFileLocked()
            # Connect to storage.
            self.conn = Connection(
                self.storage, cache_size=self._cache_size)
            self._is_open = True

    def pack(self):
        """Pack the underlying storage."""
        self.conn.pack()

    def rollback(self):
        """Abort the current transaction."""
        self.conn.abort()
