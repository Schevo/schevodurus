"""Durus backend.

For copyright, license, and warranty, see bottom of file.
"""

from durus.btree import BTree
## from durus.client_storage import ClientStorage
from durus.connection import Connection
from durus.file_storage import FileStorage, ShelfStorage
from durus.persistent_dict import PersistentDict
from durus.persistent_list import PersistentList

from schevodurus.backend_test_classes import (
    TestMethods_CreatesDatabase,
    TestMethods_CreatesSchema,
    TestMethods_EvolvesSchemata,
    )


DEFAULT_CACHE_SIZE = 100000


class DurusBackend(object):

    description = 'Backend that directly uses Durus 3.7'
    backend_args_help = """
    cache_size=SIZE
        Set the size of the in-memory object cache to SIZE, which is an
        integer specifying the maximum number of objects to keep in the
        cache.
    storage=TYPE
        Set the type of storage to use when creating a new database.
        Two types of storage are available:
        - 'shelf' (default) decreases startup time and reduces memory
          pressure by using the durus.file_storage.ShelfStorage class.
        - 'file' uses the traditional durus.file_storage.FileStorage class.
    """

    __test__ = False

    BTree = BTree
    PDict = PersistentDict
    PList = PersistentList

    TestMethods_CreatesDatabase = TestMethods_CreatesDatabase
    TestMethods_CreatesSchema = TestMethods_CreatesSchema
    TestMethods_EvolvesSchemata = TestMethods_EvolvesSchemata

    def __init__(self, filename, storage='shelf',
                 cache_size=DEFAULT_CACHE_SIZE):
        """Create a new `DurussBackend` instance.

        - `filename`: Name of file to open with this backend.
        - `storage`: Type of Durus storage to use.  May be either
          `'shelf'` or `'file'`. `'shelf'` has shorter startup time
          for a packed database and is the default.
        - `cache_size`: Maximum number of objects to keep in the
          in-memory object cache.
        """
        self._filename = filename
        self._storage = storage
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
        header = f.read(128)
        f.close()
        # Look for Durus file storage or shelf storage signature and
        # durus module signature.
        if 'durus.persistent_dict' in header:
            if header[:5] == 'DFS20':
                return (True, dict(storage='file'))
            elif header[:7] == 'SHELF-1':
                return (True, dict(storage='shelf'))
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
            self.storage = getattr(self, '_open_' + self._storage)(
                self._filename)
            self.conn = Connection(self.storage, cache_size=self._cache_size)
            self._is_open = True

    def _open_file(self, filename):
        return FileStorage(filename)

    def _open_shelf(self, filename):
        return ShelfStorage(filename)

    def pack(self):
        """Pack the underlying storage."""
        self.conn.pack()

    def rollback(self):
        """Abort the current transaction."""
        self.conn.abort()


# Copyright (C) 2001-2006 Orbtech, L.L.C.
#
# Schevo
# http://schevo.org/
#
# Orbtech
# 709 East Jackson Road
# Saint Louis, MO  63119-4241
# http://orbtech.com/
#
# This toolkit is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This toolkit is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA