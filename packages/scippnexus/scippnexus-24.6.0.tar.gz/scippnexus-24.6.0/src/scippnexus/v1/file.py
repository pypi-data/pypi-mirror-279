# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2023 Scipp contributors (https://github.com/scipp)
# @author Simon Heybrock
import warnings
from contextlib import AbstractContextManager

import h5py
from scipp import VisibleDeprecationWarning

from .nexus_classes import NXroot


class File(AbstractContextManager, NXroot):
    def __init__(self, *args, definition=None, **kwargs):
        warnings.warn(
            "The scippnexus.v1 API is deprecated and will be removed in release 24.01. "
            "Switch to 'import scippnexus as snx' to use API version 2.",
            VisibleDeprecationWarning,
            stacklevel=2,
        )
        self._file = h5py.File(*args, **kwargs)
        NXroot.__init__(self, self._file, definition=definition)

    def __enter__(self):
        self._file.__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._file.close()

    def close(self):
        self._file.close()
