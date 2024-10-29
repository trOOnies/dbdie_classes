"""Implemented full model types."""

from dbdie_classes.options import KILLER_FMT
from dbdie_classes.options import SURV_FMT

FMTS = [
    KILLER_FMT.ADDONS,
    SURV_FMT.ADDONS,
    KILLER_FMT.CHARACTER,
    SURV_FMT.CHARACTER,
    KILLER_FMT.ITEM,
    SURV_FMT.ITEM,
    KILLER_FMT.OFFERING,
    SURV_FMT.OFFERING,
    KILLER_FMT.PERKS,
    SURV_FMT.PERKS,
    SURV_FMT.STATUS,
]
