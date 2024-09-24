"""Player type, i.e. 'killer', 'surv' or None."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dbdie_classes.base import IsForKiller, PlayerType

SURV:   "PlayerType" = "surv"
KILLER: "PlayerType" = "killer"

ALL: list["PlayerType"] = [SURV, KILLER]


def ifk_to_pt(ifk: "IsForKiller") -> "PlayerType":
    """Killer boolean ('is for killer') to PlayerType."""
    return ALL[int(ifk)] if ifk is not None else None


def pt_to_ifk(pt: "PlayerType") -> "IsForKiller":
    """PlayerType to killer boolean ('is for killer')."""
    return (pt == KILLER) if pt is not None else None
