"""Implemented full model types."""

from dbdie_classes.options import KILLER_FMT
from dbdie_classes.options import SURV_FMT

FMTS = [
    KILLER_FMT.CHARACTER,
    SURV_FMT.CHARACTER,
    KILLER_FMT.ITEM,
    SURV_FMT.ITEM,
    KILLER_FMT.PERKS,
    SURV_FMT.PERKS,
    SURV_FMT.STATUS,
]