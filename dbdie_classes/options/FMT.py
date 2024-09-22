"""All full model types."""

from dbdie_classes.options import PLAYER_TYPE as PT
from dbdie_classes.options.COMMON_FMT import COMMON
from dbdie_classes.options.KILLER_FMT import KILLER
from dbdie_classes.options.SURV_FMT import SURV

ALL = KILLER + SURV + COMMON
ALL_DICT = {
    None: COMMON,
    PT.KILLER: KILLER,
    PT.SURV: SURV,
}
