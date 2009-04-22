"""Run tests against durus backend."""

# Copyright (c) 2001-2009 ElevenCraft Inc.
# See LICENSE for details.

import sys
from schevo.lib import optimize

from schevo.test.library import storage_classes


locals().update(storage_classes(class_label='durus-shelf-1',
                                backend_name='durus',
                                format=1,
                                backend_args=dict(storage='shelf'),
                                ))
locals().update(storage_classes(class_label='durus-shelf-2',
                                backend_name='durus',
                                format=2,
                                backend_args=dict(storage='shelf'),
                                ))
locals().update(storage_classes(class_label='durus-file-1',
                                backend_name='durus',
                                format=1,
                                backend_args=dict(storage='file'),
                                ))
locals().update(storage_classes(class_label='durus-file-2',
                                backend_name='durus',
                                format=2,
                                backend_args=dict(storage='file'),
                                ))


optimize.bind_all(sys.modules[__name__])  # Last line of module.
