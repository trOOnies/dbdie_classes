"""Columns as they appear in the SQL database."""

from dbdie_classes.options import MODEL_TYPES as MT

CHARACTER = ["character"]
PERKS     = ["perk_0", "perk_1", "perk_2", "perk_3"]
ITEM      = ["item"]
ADDONS    = ["addon_0", "addon_1"]
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
