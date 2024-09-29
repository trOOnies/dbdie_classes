"""Common full model types."""

from typing import TYPE_CHECKING

from dbdie_classes.options import MODEL_TYPE as MT

if TYPE_CHECKING:
    from dbdie_classes.base import FullModelType


POINTS   : "FullModelType" = MT.POINTS
PRESTIGE : "FullModelType" = MT.PRESTIGE

ALL: list["FullModelType"] = [
    POINTS,
    PRESTIGE,
]
