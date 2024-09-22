"""Player full model types (basically the cropped player row)."""

from dbdie_classes.options import PLAYER_TYPE as PT

SURV_PLAYER   = f"player__{PT.SURV}"
KILLER_PLAYER = f"player__{PT.KILLER}"

ALL = [
    SURV_PLAYER,
    KILLER_PLAYER,
]
