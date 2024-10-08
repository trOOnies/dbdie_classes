"""DBD version related classes."""

from __future__ import annotations

from dataclasses import dataclass, asdict

from dbdie_classes.code.version import compare_dbdv_ranges, get_max_id


@dataclass(frozen=True, eq=True, order=True)
class DBDVersion:
    """DBD game version as named by BHVR (M.m.p-ptb)"""

    major: str
    minor: str
    patch: str
    is_not_ptb: bool = True

    dict = asdict

    def __str__(self) -> str:
        return (
            f"{self.major}.{self.minor}.{self.patch}{'' if self.is_not_ptb else '-ptb'}"
        )

    @classmethod
    def from_str(cls, s: str) -> DBDVersion:
        """Instantiate DBDVersion from its string form."""
        ss = s.split(".")
        is_ptb = ss[2].endswith("-ptb")
        return DBDVersion(
            major=ss[0],
            minor=ss[1],
            patch=ss[2][:-4] if is_ptb else ss[2],
            is_not_ptb=not is_ptb,
        )

    @classmethod
    def from_schema(cls, dbdv) -> DBDVersion:
        """Instantiate DBDVersion from a sqlalchemy DBDVersionOut model."""
        return cls.from_str(dbdv.name)


@dataclass
class DBDVersionRange:
    """DBD game version range, first inclusive last exclusive."""

    id:     str
    max_id: str | None = None

    def __post_init__(self):
        self.bounded = self.max_id is not None
        self._id = DBDVersion.from_str(self.id)
        self._max_id = DBDVersion.from_str(self.max_id) if self.bounded else None
        assert (not self.bounded) or (self._id < self._max_id)

    @classmethod
    def from_dbd_versions(
        cls,
        dbd_v1: DBDVersion,
        dbd_v2: DBDVersion | None,
    ) -> DBDVersionRange:
        """Instantiate DBDVersionRange using DBDVersions."""
        return DBDVersionRange(
            id=str(dbd_v1),
            max_id=None if dbd_v2 is None else str(dbd_v2),
        )

    def __str__(self) -> str:
        return f">={self._id},<{self._max_id}" if self.bounded else f">={self._id}"

    def __eq__(self, other) -> bool:
        return (
            compare_dbdv_ranges(self, other)
            if isinstance(other, DBDVersionRange)
            else False
        )

    def __contains__(self, v: DBDVersion) -> bool:
        """Checks if a DBDVersion is contained in the DBDVersionRange."""
        return (self._id <= v) and ((not self.bounded) or (v < self._max_id))

    def __and__(self, other: DBDVersionRange) -> DBDVersionRange | None:
        """DBDVersions intersection."""
        _id = max(self._id, other._id)
        id = str(_id)
        max_id = get_max_id(self, other)

        try:
            dbd_vr = DBDVersionRange(id, max_id)
        except AssertionError:
            dbd_vr = None
        except Exception:
            raise

        return dbd_vr

    def to_list(self) -> list[str | None]:
        return [self.id, self.max_id]
