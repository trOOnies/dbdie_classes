"""Columns as they appear in the SQL database."""

from typing import TYPE_CHECKING

from dbdie_classes.options import MODEL_TYPE as MT
if TYPE_CHECKING:
    from dbdie_classes.base import SQLColumn

CHARACTER : list["SQLColumn"] = ["character"]
PERKS     : list["SQLColumn"] = ["perks_0", "perks_1", "perks_2", "perks_3"]
ITEM      : list["SQLColumn"] = ["item"]
ADDONS    : list["SQLColumn"] = ["addons_0", "addons_1"]
OFFERING  : list["SQLColumn"] = ["offering"]
STATUS    : list["SQLColumn"] = ["status"]
POINTS    : list["SQLColumn"] = ["points"]
PRESTIGE  : list["SQLColumn"] = ["prestige"]

ALL = [
    CHARACTER,
    PERKS,
    ITEM,
    ADDONS,
    OFFERING,
    STATUS,
    # POINTS,
    # PRESTIGE,
]
ALL_FLATTENED = sum((cols for cols in ALL), [])

MT_TO_COLS = {
    MT.CHARACTER: CHARACTER,
    MT.PERKS: PERKS,
    MT.ITEM: ITEM,
    MT.ADDONS: ADDONS,
    MT.OFFERING: OFFERING,
    MT.STATUS: STATUS,
    # MT.POINTS: POINTS,
    # MT.PRESTIGE: PRESTIGE,
}

MANUALLY_CHECKED_COLS: list["SQLColumn"] = [f"{mt}_mckd" for mt in MT.ALL]
