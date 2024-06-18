# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2023 Scipp contributors (https://github.com/scipp)
# @author Simon Heybrock
from __future__ import annotations

from typing import List, Optional, Union
from warnings import warn

import numpy as np
import scipp as sc

from .._common import to_child_select
from ..typing import H5Group
from .nxcylindrical_geometry import NXcylindrical_geometry
from .nxobject import Field, NexusStructureError, NXobject, ScippIndex, asarray
from .nxoff_geometry import NXoff_geometry
from .nxtransformations import NXtransformations


class NXdataStrategy:
    """
    Strategy used by :py:class:`scippnexus.NXdata`.

    May be subclassed to customize behavior.
    """

    _error_suffixes = ["_errors", "_error"]  # _error is the deprecated suffix

    @staticmethod
    def axes(group):
        """Names of the axes (dimension labels)."""
        return group.attrs.get("axes")

    @staticmethod
    def signal(group):
        """Name of the signal field."""
        if (name := group.attrs.get("signal")) is not None:
            if name in group:
                return name
        # Legacy NXdata defines signal not as group attribute, but attr on dataset
        for name in group.keys():
            # What is the meaning of the attribute value? It is undocumented, we simply
            # ignore it.
            if "signal" in group._get_child(name).attrs:
                return name
        return None

    @staticmethod
    def signal_errors(group) -> str | None:
        """Name of the field to use for standard-deviations of the signal."""
        name = f"{NXdataStrategy.signal(group)}_errors"
        if name in group:
            return name
        # This is a legacy named, deprecated in the NeXus format.
        if "errors" in group:
            return "errors"

    @staticmethod
    def coord_errors(group, name):
        """Name of the field to use for standard-deviations of a coordinate."""
        errors = [f"{name}{suffix}" for suffix in NXdataStrategy._error_suffixes]
        errors = [x for x in errors if x in group]
        if len(errors) == 0:
            return None
        if len(errors) == 2:
            warn(
                f"Found {name}_errors as well as the deprecated "
                f"{name}_error. The latter will be ignored."
            )
        return errors[0]


class NXdata(NXobject):
    def __init__(
        self,
        group: H5Group,
        *,
        definition=None,
        strategy=None,
        signal_override: Field | _EventField = None,  # noqa: F821
        skip: list[str] = None,
    ):
        """
        Parameters
        ----------
        signal_override:
            Field-like to use instead of trying to read signal from the file. This is
            used when there is no signal or to provide a signal computed from
            NXevent_data.
        skip:
            Names of fields to skip when loading coords.
        """
        super().__init__(group, definition=definition, strategy=strategy)
        self._signal_override = signal_override
        self._skip = skip if skip is not None else []

    def _default_strategy(self):
        return NXdataStrategy

    @property
    def shape(self) -> list[int]:
        return self._signal.shape

    def _get_group_dims(self) -> None | list[str]:
        # Apparently it is not possible to define dim labels unless there are
        # corresponding coords. Special case of '.' entries means "no coord".
        if (axes := self._strategy.axes(self)) is not None:
            return [f"dim_{i}" if a == "." else a for i, a in enumerate(axes)]
        axes = []
        # Names of axes that have an "axis" attribute serve as dim labels in legacy case
        for name, field in self._group.items():
            if (axis := field.attrs.get("axis")) is not None:
                axes.append((axis, name))
        if axes:
            return [x[1] for x in sorted(axes)]
        return None

    @property
    def dims(self) -> list[str]:
        if (d := self._get_group_dims()) is not None:
            return d
        # Legacy NXdata defines axes not as group attribute, but attr on dataset.
        # This is handled by class Field.
        return self._signal.dims

    @property
    def unit(self) -> sc.Unit | None:
        return self._signal.unit

    @property
    def _signal_name(self) -> str:
        return self._strategy.signal(self)

    @property
    def _errors_name(self) -> str | None:
        return self._strategy.signal_errors(self)

    @property
    def _signal(self) -> Field | _EventField | None:  # noqa: F821
        if self._signal_override is not None:
            return self._signal_override
        if self._signal_name is not None:
            if self._signal_name not in self:
                raise NexusStructureError(
                    f"Signal field '{self._signal_name}' not found in group."
                )
            return self[self._signal_name]
        return None

    def _get_axes(self):
        """Return labels of named axes. Does not include default 'dim_{i}' names."""
        if (axes := self._strategy.axes(self)) is not None:
            # Unlike self.dims we *drop* entries that are '.'
            return [a for a in axes if a != "."]
        elif (signal := self._signal) is not None:
            if (axes := signal.attrs.get("axes")) is not None:
                dims = axes.split(":")
                # The standard says that the axes should be colon-separated, but some
                # files use comma-separated.
                if len(dims) == 1 and self._signal.ndim > 1:
                    dims = tuple(axes.split(","))
                return dims
        return []

    def _guess_dims(self, name: str):
        """Guess dims of non-signal dataset based on shape.

        Does not check for potential bin-edge coord.
        """
        shape = self._get_child(name).shape
        if self.shape == shape:
            return self.dims
        lut = {}
        if self._signal is not None:
            for d, s in zip(self.dims, self.shape):
                if self.shape.count(s) == 1:
                    lut[s] = d
        try:
            dims = [lut[s] for s in shape]
        except KeyError:
            raise NexusStructureError(
                f"Could not determine axis indices for {self.name}/{name}"
            )
        return dims

    def _try_guess_dims(self, name):
        try:
            return self._guess_dims(name)
        except NexusStructureError:
            return None

    def _get_field_dims(self, name: str) -> None | list[str]:
        # Newly written files should always contain indices attributes, but the
        # standard recommends that readers should also make "best effort" guess
        # since legacy files do not set this attribute.
        if (indices := self.attrs.get(f"{name}_indices")) is not None:
            return list(np.array(self.dims)[np.array(indices).flatten()])
        if (axis := self._get_child(name).attrs.get("axis")) is not None:
            return (self._get_group_dims()[axis - 1],)
        if name in [self._signal_name, self._errors_name]:
            return self._get_group_dims()  # if None, field determines dims itself
        if name in list(self.attrs.get("auxiliary_signals", [])):
            return self._try_guess_dims(name)
        if name in self._get_axes():
            # If there are named axes then items of same name are "dimension
            # coordinates", i.e., have a dim matching their name.
            # However, if the item is not 1-D we need more labels. Try to use labels of
            # signal if dimensionality matches.
            if self._signal_name in self and self._get_child(name).ndim == len(
                self.shape
            ):
                return self[self._signal_name].dims
            return [name]
        return self._try_guess_dims(name)

    def _bin_edge_dim(self, coord: Field) -> None | str:
        sizes = dict(zip(self.dims, self.shape))
        for dim, size in zip(coord.dims, coord.shape):
            if dim in sizes and sizes[dim] + 1 == size:
                return dim
        return None

    def _dim_of_coord(self, name: str, coord: Field) -> None | str:
        if len(coord.dims) == 1:
            return coord.dims[0]
        if name in coord.dims and name in self.dims:
            return name
        return self._bin_edge_dim(coord)

    def _should_be_aligned(self, da: sc.DataArray, name: str, coord: Field) -> bool:
        dim_of_coord = self._dim_of_coord(name, coord)
        if dim_of_coord is None:
            return True
        if dim_of_coord not in da.dims:
            return False
        return True

    def _getitem(self, select: ScippIndex) -> sc.DataArray:
        from .nexus_classes import NXgeometry

        signal = self._signal
        if signal is None:
            raise NexusStructureError("No signal field found, cannot load group.")
        signal = signal[select]
        if self._errors_name is not None:
            stddevs = self[self._errors_name][select]
            # According to the standard, errors must have the same shape as the data.
            # This is not the case in all files we observed, is there any harm in
            # attempting a broadcast?
            signal.variances = np.broadcast_to(
                sc.pow(stddevs, sc.scalar(2)).values, shape=signal.shape
            )

        da = (
            signal
            if isinstance(signal, sc.DataArray)
            else sc.DataArray(data=asarray(signal))
        )

        skip = self._skip
        skip += [self._signal_name, self._errors_name]
        skip += list(self.attrs.get("auxiliary_signals", []))
        for name in self:
            if (errors := self._strategy.coord_errors(self, name)) is not None:
                skip += [errors]
        for name in self:
            if name in skip:
                continue
            # It is not entirely clear whether skipping NXtransformations is the right
            # solution. In principle NXobject will load them via the 'depends_on'
            # mechanism, so for valid files this should be sufficient.
            allowed = (
                Field,
                NXtransformations,
                NXcylindrical_geometry,
                NXoff_geometry,
                NXgeometry,
            )
            if not isinstance(self._get_child(name), allowed):
                raise NexusStructureError(
                    "Invalid NXdata: may not contain nested groups"
                )

        for name, field in self[Field].items():
            if name in skip:
                continue
            sel = to_child_select(
                self.dims, field.dims, select, bin_edge_dim=self._bin_edge_dim(field)
            )
            coord: sc.Variable = asarray(self[name][sel])
            if (error_name := self._strategy.coord_errors(self, name)) is not None:
                stddevs = asarray(self[error_name][sel])
                coord.variances = sc.pow(stddevs, sc.scalar(2)).values
            try:
                da.coords[name] = coord
                da.coords.set_aligned(name, self._should_be_aligned(da, name, field))
            except sc.DimensionError as e:
                raise NexusStructureError(
                    f"Field in NXdata incompatible with dims or shape of signal: {e}"
                ) from e

        return da
