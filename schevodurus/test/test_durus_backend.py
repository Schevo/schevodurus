"""Run tests against durus backend."""

# Copyright (c) 2001-2009 ElevenCraft Inc.
# See LICENSE for details.

import sys
from schevo.lib import optimize

from schevo.test.library import storage_classes


locals().update(storage_classes(class_label='durus-1',
                                backend_name='durus',
                                format=1,
                                ))
locals().update(storage_classes(class_label='durus-2',
                                backend_name='durus',
                                format=2,
                                ))


optimize.bind_all(sys.modules[__name__])  # Last line of module.
