"""All full model types."""

from copy import deepcopy
from typing import TYPE_CHECKING

from dbdie_classes.options import MODEL_TYPE as MT
from dbdie_classes.options import PLAYER_TYPE as PT
from dbdie_classes.options.COMMON_FMT import ALL as COMMON
from dbdie_classes.options.KILLER_FMT import ALL as KILLER
from dbdie_classes.options.SURV_FMT import ALL as SURV

if TYPE_CHECKING:
    from dbdie_classes.base import FullModelType, IsForKiller, ModelType, PlayerType

ALL = KILLER + SURV + COMMON
ALL_DICT = {
    None: COMMON,
    PT.KILLER: KILLER,
    PT.SURV: SURV,
}


def extract_mt_pt_ifk(
    fmt: "FullModelType",
) -> tuple["ModelType", "PlayerType", "IsForKiller"]:
    """Extract ModelType, PlayerType, and IsForKiller from FullModelType."""
    ix = fmt.find("__")
    if ix > -1:
        pt = fmt[ix + 2:]
        return fmt[:ix], pt, pt == PT.KILLER
    else:
        return deepcopy(fmt), None, None


def assert_mt_and_pt(mt: str, pt: str | None) -> None:
    assert mt in MT.ALL, f"'{mt}' is not a valid model type"
    assert (pt is None) or (pt in PT.ALL), "Value must be 'killer', 'surv' or None"


def extract_mts_pts_ifks(
    fmts: list["FullModelType"]
) -> tuple[list["ModelType"], list["PlayerType"], list["IsForKiller"]]:
    """Extract ModelTypes, PlayerTypes, and IsForKillers from list of FullModelTypes."""
    mts_and_pts = [extract_mt_pt_ifk(fmt) for fmt in fmts]
    return (
        [tup[0] for tup in mts_and_pts],
        [tup[1] for tup in mts_and_pts],
        [tup[2] for tup in mts_and_pts],
    )


def to_fmt(mt: "ModelType", ifk: "IsForKiller") -> "FullModelType":
    """Convert model type and killer boolean to full model type."""
    return mt + ("" if ifk is None else f"__{PT.ifk_to_pt(ifk)}")
