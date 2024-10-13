"""Columns as they appear in the SQL database."""

from dbdie_classes.options import MODEL_TYPE as MT

CHARACTER = ["character"]
PERKS     = ["perks_0", "perks_1", "perks_2", "perks_3"]
ITEM      = ["item"]
ADDONS    = ["addons_0", "addons_1"]
OFFERING  = ["offering"]
STATUS    = ["status"]
POINTS    = ["points"]
PRESTIGE  = ["prestige"]

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

MANUALLY_CHECKED_COLS = [f"{mt}_mckd" for mt in MT.ALL]
