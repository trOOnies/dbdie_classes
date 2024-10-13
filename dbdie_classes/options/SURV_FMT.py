"""Survivor full model types."""

from typing import TYPE_CHECKING

from dbdie_classes.options import MODEL_TYPE as MT
from dbdie_classes.options.PLAYER_TYPE import SURV

if TYPE_CHECKING:
    from dbdie_classes.base import FullModelType

ADDONS    : "FullModelType" = f"{MT.ADDONS}__{SURV}"
CHARACTER : "FullModelType" = f"{MT.CHARACTER}__{SURV}"
ITEM      : "FullModelType" = f"{MT.ITEM}__{SURV}"
OFFERING  : "FullModelType" = f"{MT.OFFERING}__{SURV}"
PERKS     : "FullModelType" = f"{MT.PERKS}__{SURV}"
STATUS    : "FullModelType" = f"{MT.STATUS}__{SURV}"

ALL: list["FullModelType"] = [
    ADDONS,
    CHARACTER,
    ITEM,
    OFFERING,
    PERKS,
    STATUS,
]  # ! order is maintained for SQL
