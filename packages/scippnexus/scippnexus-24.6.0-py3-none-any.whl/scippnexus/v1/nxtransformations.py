# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2023 Scipp contributors (https://github.com/scipp)
# @author Simon Heybrock
from __future__ import annotations

from typing import List, Optional, Union

import numpy as np
import scipp as sc
from scipp.scipy import interpolate

from .nxobject import Field, NexusStructureError, NXobject, ScippIndex


class TransformationError(NexusStructureError):
    pass


def make_transformation(obj, /, path) -> Transformation | None:
    if path.startswith("/"):
        return Transformation(obj.file[path])
    elif path != ".":
        return Transformation(obj.parent[path])
    return None  # end of chain


class NXtransformations(NXobject):
    """Group of transformations."""

    def _getitem(self, index: ScippIndex) -> sc.DataGroup:
        return sc.DataGroup(
            {
                name: get_full_transformation_starting_at(
                    Transformation(child), index=index
                )
                for name, child in self.items()
            }
        )


class Transformation:
    def __init__(self, obj: Field | NXobject):  # could be an NXlog
        self._obj = obj

    @property
    def attrs(self):
        return self._obj.attrs

    @property
    def name(self):
        return self._obj.name

    @property
    def depends_on(self):
        if (path := self.attrs.get("depends_on")) is not None:
            return make_transformation(self._obj, path)
        return None

    @property
    def offset(self):
        if (offset := self.attrs.get("offset")) is None:
            return None
        if (offset_units := self.attrs.get("offset_units")) is None:
            raise TransformationError(
                f"Found {offset=} but no corresponding 'offset_units' "
                f"attribute at {self.name}"
            )
        return sc.spatial.translation(value=offset, unit=offset_units)

    @property
    def vector(self) -> sc.Variable:
        return sc.vector(value=self.attrs.get("vector"))

    def __getitem__(self, select: ScippIndex):
        transformation_type = self.attrs.get("transformation_type")
        # According to private communication with Tobias Richter, NeXus allows 0-D or
        # shape=[1] for single values. It is unclear how and if this could be
        # distinguished from a scan of length 1.
        value = self._obj[select]
        try:
            if isinstance(value, sc.DataGroup):
                raise TransformationError(
                    f"Failed to load transformation at {self.name}."
                )
            t = value * self.vector
            v = t if isinstance(t, sc.Variable) else t.data
            if transformation_type == "translation":
                v = v.to(unit="m", copy=False)
                v = sc.spatial.translations(dims=v.dims, values=v.values, unit=v.unit)
            elif transformation_type == "rotation":
                v = sc.spatial.rotations_from_rotvecs(v)
            else:
                raise TransformationError(
                    f"{transformation_type=} attribute at {self.name},"
                    " expected 'translation' or 'rotation'."
                )
            if isinstance(t, sc.Variable):
                t = v
            else:
                t.data = v
            if (offset := self.offset) is None:
                return t
            offset = sc.vector(value=offset.values, unit=offset.unit).to(unit="m")
            offset = sc.spatial.translation(value=offset.value, unit=offset.unit)
            return t * offset
        except (sc.DimensionError, sc.UnitError) as e:
            raise NexusStructureError(
                f"Invalid transformation in NXtransformations: {e}"
            ) from e


def _interpolate_transform(transform, xnew):
    # scipy can't interpolate with a single value
    if transform.sizes["time"] == 1:
        transform = sc.concat([transform, transform], dim="time")
    return interpolate.interp1d(
        transform, "time", kind="previous", fill_value="extrapolate"
    )(xnew=xnew)


def _smaller_unit(a, b):
    if a.unit == b.unit:
        return a.unit
    ratio = sc.scalar(1.0, unit=a.unit).to(unit=b.unit)
    if ratio.value < 1.0:
        return a.unit
    else:
        return b.unit


def get_full_transformation(
    depends_on: Field,
) -> None | sc.DataArray | sc.Variable:
    """
    Get the 4x4 transformation matrix for a component, resulting
    from the full chain of transformations linked by "depends_on"
    attributes
    """
    if (t0 := make_transformation(depends_on, depends_on[()])) is None:
        return None
    return get_full_transformation_starting_at(t0)


def get_full_transformation_starting_at(
    t0: Transformation, *, index: ScippIndex = None
) -> None | sc.DataArray | sc.Variable:
    transformations = _get_transformations(t0, index=() if index is None else index)

    total_transform = None
    for transform in transformations:
        if total_transform is None:
            total_transform = transform
        elif isinstance(total_transform, sc.DataArray) and isinstance(
            transform, sc.DataArray
        ):
            unit = _smaller_unit(
                transform.coords["time"], total_transform.coords["time"]
            )
            total_transform.coords["time"] = total_transform.coords["time"].to(
                unit=unit, copy=False
            )
            transform.coords["time"] = transform.coords["time"].to(
                unit=unit, copy=False
            )
            time = sc.concat(
                [total_transform.coords["time"], transform.coords["time"]], dim="time"
            )
            time = sc.datetimes(values=np.unique(time.values), dims=["time"], unit=unit)
            total_transform = _interpolate_transform(
                transform, time
            ) * _interpolate_transform(total_transform, time)
        else:
            total_transform = transform * total_transform
    if isinstance(total_transform, sc.DataArray):
        time_dependent = [t for t in transformations if isinstance(t, sc.DataArray)]
        times = [da.coords["time"][0] for da in time_dependent]
        latest_log_start = sc.reduce(times).max()
        return total_transform["time", latest_log_start:].copy()
    return total_transform


def _get_transformations(
    transform: Transformation, *, index: ScippIndex
) -> list[sc.DataArray | sc.Variable]:
    """Get all transformations in the depends_on chain."""
    transformations = []
    t = transform
    while t is not None:
        transformations.append(t[index])
        t = t.depends_on
    # TODO: this list of transformation should probably be cached in the future
    # to deal with changing beamline components (e.g. pixel positions) during a
    # live data stream (see https://github.com/scipp/scippneutron/issues/76).
    return transformations
