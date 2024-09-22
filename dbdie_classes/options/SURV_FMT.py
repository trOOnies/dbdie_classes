"""Survivor full model types."""

from dbdie_classes.options import MODEL_TYPE as MT
from dbdie_classes.options.PLAYER_TYPE import SURV as PT_SURV

ADDONS    = f"{MT.ADDONS}__{PT_SURV}"
CHARACTER = f"{MT.CHARACTER}__{PT_SURV}"
ITEM      = f"{MT.ITEM}__{PT_SURV}"
OFFERING  = f"{MT.OFFERING}__{PT_SURV}"
PERKS     = f"{MT.PERKS}__{PT_SURV}"
STATUS    = f"{MT.STATUS}__{PT_SURV}"

SURV = [
    ADDONS,
    CHARACTER,
    ITEM,
    OFFERING,
    PERKS,
    STATUS,
]
