"""Pydantic schemas for the helper classes."""

from __future__ import annotations

import datetime as dt
from pydantic import BaseModel, Field, NonNegativeInt, StrictBool

from dbdie_classes.code.version import (
    check_type,
    compare_dbdv_ranges,
    intersect_dbdv_max,
    is_left_to,
)


class DBDVersionCreate(BaseModel):
    """DBD game version creation schema (M.m.p-ptb)."""

    name         : str            = Field(..., description="Game full patch identification")
    common_name  : str | None     = Field(..., description="Common name for the patch")
    release_date : dt.date | None = Field(..., description="Patch release date")

    @property
    def is_ptb(self) -> bool:
        return self.name.endswith("-ptb")

    @property
    def base_version(self) -> str:
        return self.name[:-4] if self.is_ptb else self.name

    @property
    def major(self) -> str:
        return self.base_version.split(".")[0]

    @property
    def minor(self) -> str:
        return self.base_version.split(".")[1]

    @property
    def patch(self) -> str:
        return self.base_version.split(".")[2]

    @property
    def info_tuple(self) -> tuple[str, str, str, bool]:
        M, m, p = self.base_version.split(".")
        return M, m, p, self.is_ptb


def coalesce(other, cond: bool, else_val: bool) -> bool:
    return cond if other is not None else else_val


class DBDVersionOut(DBDVersionCreate):
    """DBD game version output schema (M.m.p-ptb).

    Since new implementation, it can now be compared to a None value,
    which represents an 'infinitely large id number' that is used
    for an unbounded `DBDVersionRange`.
    """

    id: NonNegativeInt

    @classmethod
    def from_model(cls, dbdv) -> DBDVersionOut:
        """Instantiate `DBDVersionOut` from a sqlalchemy `DBDVersion` model."""
        return cls(
            id=dbdv.id,
            name=dbdv.name,
            release_date=dbdv.release_date,
            common_name=dbdv.common_name,
        )

    def __eq__(self, other) -> bool:
        check_type(other, DBDVersionOut, allow_none=True)
        return coalesce(other, self.id == other.id, else_val=False)

    def __ne__(self, other) -> bool:
        check_type(other, DBDVersionOut, allow_none=True)
        return coalesce(other, self.id != other.id, else_val=True)

    def __le__(self, other) -> bool:
        check_type(other, DBDVersionOut, allow_none=True)
        return coalesce(other, self.id <= other.id, else_val=True)

    def __lt__(self, other) -> bool:
        check_type(other, DBDVersionOut, allow_none=True)
        return coalesce(other, self.id < other.id, else_val=True)

    def __ge__(self, other) -> bool:
        check_type(other, DBDVersionOut, allow_none=True)
        return coalesce(other, self.id >= other.id, else_val=False)

    def __gt__(self, other) -> bool:
        check_type(other, DBDVersionOut, allow_none=True)
        return coalesce(other, self.id > other.id, else_val=False)


class DBDVersionRange(BaseModel):
    """DBD game version range, first inclusive last exclusive.

    Since new implementation, it can now be compared to a None value,
    which represents an empty `DBDVersionRange` that is used
    for null intersections between `DBDVersionRanges`.
    """

    dbdv_min: DBDVersionOut        = Field(..., description="Range minimum version (inclusive)")
    dbdv_max: DBDVersionOut | None = Field(..., description="Range maximum version (exclusive)")
    bounded:  StrictBool = True  # ! do not use as input

    def model_post_init(self, __context):
        self.bounded = self.dbdv_max is not None
        assert (not self.bounded) or (self.dbdv_min.id < self.dbdv_max.id)

    def __repr__(self) -> str:
        return f"DBDVersionRange({self.dbdv_min.name}, {self.dbdv_max.name})"

    def __str__(self) -> str:
        return (
            f">={self.dbdv_min.name},<{self.dbdv_max.name}"
            if self.bounded
            else f">={self.dbdv_min.name}"
        )

    def __eq__(self, other) -> bool:
        check_type(other, DBDVersionRange, allow_none=True)
        return compare_dbdv_ranges(self, other)

    def __contains__(self, dbdv: DBDVersionOut | None) -> bool:
        """Checks if a `DBDVersionOut` is contained in the `DBDVersionRange`."""
        if dbdv is None:
            return not self.bounded

        return (
            (self.dbdv_min <= dbdv)
            and ((not self.bounded) or (dbdv < self.dbdv_max))
        )

    def __and__(self, other: DBDVersionRange | None) -> DBDVersionRange | None:
        """Return the intersection range of the `DBDVersionRanges`."""
        if other is None:
            return None

        if is_left_to(self, other) or is_left_to(other, self):
            return None

        dbdv_min = (
            self.dbdv_min
            if other.dbdv_min < self.dbdv_min
            else other.dbdv_min
        )
        dbdv_max = intersect_dbdv_max(self, other)
        return DBDVersionRange(dbdv_min, dbdv_max)

    @classmethod
    def from_dicts(cls, dbdv_min: dict, dbdv_max: dict | None) -> DBDVersionRange:
        """Create a `DBDVersionRange` from its dict definitions."""
        return cls(
            dbdv_min=DBDVersionOut(**dbdv_min),
            dbdv_max=DBDVersionOut(**dbdv_max) if dbdv_max is not None else None,
        )

    def to_list(self) -> list[str | None]:
        """To 2-list of DBDVersionOut names."""
        return [self.dbdv_min.name, self.dbdv_max.name if self.bounded else None]

    def to_ids(self) -> list[int | None]:
        """To 2-list of DBDVersionOut ids."""
        return [self.dbdv_min.id, self.dbdv_max.id if self.bounded else None]
