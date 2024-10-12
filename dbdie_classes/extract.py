"""DBDIE classes for extract purposes."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dbdie_classes.base import CropCoordsRaw, ImgSize, LabelId, PlayerId


@dataclass(eq=True)
class CropCoords:
    """Crop coordinates in relation to its source image or crop."""

    left:   int
    top:    int
    right:  int
    bottom: int
    index:  int = 0

    def raw(self) -> "CropCoordsRaw":
        """Get crop in raw fom: 4-int-tuple LTRB."""
        return (self.left, self.top, self.right, self.bottom)

    def __iter__(self):
        return self

    def __next__(self):
        try:
            result = self.raw()[self.index]
        except IndexError:
            raise StopIteration
        self.index += 1
        return result

    @property
    def shape(self) -> "ImgSize":
        """Shape of crop as a (width, height) tuple."""
        return (self.right - self.left, self.bottom - self.top)

    @property
    def size(self) -> int:
        """Size of crop in square px."""
        return (self.right - self.left) * (self.bottom - self.top)

    def is_fully_inside(self, cc: CropCoords) -> bool:
        """Check if the crop is fully inside the 'cc' crop."""
        return (
            (cc.left <= self.left)
            and (self.right <= cc.right)
            and (cc.top <= self.top)
            and (self.bottom <= cc.bottom)
        )

    def check_overlap(self, cc: CropCoords) -> bool:
        """Check if 2 crops of the SAME SIZE overlap."""
        return not (
            (cc.right <= self.left)
            or (self.right <= cc.left)
            or (cc.bottom <= self.top)
            or (self.bottom <= cc.top)
        )


@dataclass
class PlayerInfo:
    """Integer-encoded DBD information of a player snippet."""

    character_id: "LabelId"
    perks_ids:    tuple["LabelId", "LabelId", "LabelId", "LabelId"]
    item_id:      "LabelId"
    addons_ids:   tuple["LabelId", "LabelId"]
    offering_id:  "LabelId"
    status_id:    "LabelId"
    points:       int
    prestige:     int


PlayersCropCoords = dict["PlayerId", CropCoords]
PlayersInfoDict   = dict["PlayerId", PlayerInfo]
