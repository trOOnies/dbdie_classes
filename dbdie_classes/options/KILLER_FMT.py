"""Killer full model types."""

from typing import TYPE_CHECKING

from dbdie_classes.options import MODEL_TYPE as MT
from dbdie_classes.options.PLAYER_TYPE import KILLER

if TYPE_CHECKING:
    from dbdie_classes.base import FullModelType

ADDONS    : "FullModelType" = f"{MT.ADDONS}__{KILLER}"
CHARACTER : "FullModelType" = f"{MT.CHARACTER}__{KILLER}"
ITEM      : "FullModelType" = f"{MT.ITEM}__{KILLER}"
OFFERING  : "FullModelType" = f"{MT.OFFERING}__{KILLER}"
PERKS     : "FullModelType" = f"{MT.PERKS}__{KILLER}"

ALL: list["FullModelType"] = [
    ADDONS,
    CHARACTER,
    ITEM,
    OFFERING,
    PERKS,
]
