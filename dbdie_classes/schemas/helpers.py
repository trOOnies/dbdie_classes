"""Pydantic schemas for the helper classes."""

from __future__ import annotations

import datetime as dt
from pydantic import BaseModel

from dbdie_classes.code.version import (
    check_type, compare_dbdv_ranges, intersect_max_ids, is_left_to
)


class DBDVersionCreate(BaseModel):
    """DBD game version creation schema (M.m.p-ptb)."""

    name         : str
    common_date  : str | None
    release_date : dt.date | None

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


class DBDVersionOut(DBDVersionCreate):
    """DBD game version output schema (M.m.p-ptb).

    Since new implementation, it can now be compared to a None value,
    which represents an 'infinitely large id number' that is used
    for an unbounded `DBDVersionRange`.
    """

    id: int

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
        return (
            self.id == other.id
            if other is not None
            else False
        )

    def __ne__(self, other) -> bool:
        check_type(other, DBDVersionOut, allow_none=True)
        return (
            self.id != other.id
            if other is not None
            else True
        )

    def __le__(self, other) -> bool:
        check_type(other, DBDVersionOut, allow_none=True)
        return (
            self.id <= other.id
            if other is not None
            else True
        )

    def __lt__(self, other) -> bool:
        check_type(other, DBDVersionOut, allow_none=True)
        return (
            self.id < other.id
            if other is not None
            else True
        )

    def __ge__(self, other) -> bool:
        check_type(other, DBDVersionOut, allow_none=True)
        return (
            self.id >= other.id
            if other is not None
            else False
        )

    def __gt__(self, other) -> bool:
        check_type(other, DBDVersionOut, allow_none=True)
        return (
            self.id > other.id
            if other is not None
            else False
        )


class DBDVersionRange(BaseModel):
    """DBD game version range, first inclusive last exclusive.

    Since new implementation, it can now be compared to a None value,
    which represents an empty `DBDVersionRange` that is used
    for null intersections between `DBDVersionRanges`.
    """

    dbdv_min: DBDVersionOut
    dbdv_max: DBDVersionOut | None

    def model_post_init(self):
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
        """`DBDVersionRanges` intersection."""
        if other is None:
            return None

        if is_left_to(self, other) or is_left_to(other, self):
            return None

        dbdv_min = (
            self.dbdv_min
            if other.dbdv_min < self.dbdv_min
            else other.dbdv_min
        )
        dbdv_max = intersect_max_ids(self, other)
        return DBDVersionRange(dbdv_min, dbdv_max)

    def to_list(self) -> list[str | None]:
        """To 2-list of DBDVersionOut names."""
        return [self.dbdv_min.name, self.dbdv_max.name if self.bounded else None]
