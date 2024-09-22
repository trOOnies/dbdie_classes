"""Killer full model types."""

from dbdie_classes.options import MODEL_TYPE as MT
from dbdie_classes.options.PLAYER_TYPE import KILLER as PT_KILLER

ADDONS    = f"{MT.ADDONS}__{PT_KILLER}"
CHARACTER = f"{MT.CHARACTER}__{PT_KILLER}"
ITEM      = f"{MT.ITEM}__{PT_KILLER}"
OFFERING  = f"{MT.OFFERING}__{PT_KILLER}"
PERKS     = f"{MT.PERKS}__{PT_KILLER}"

KILLER = [
    ADDONS,
    CHARACTER,
    ITEM,
    OFFERING,
    PERKS,
]
