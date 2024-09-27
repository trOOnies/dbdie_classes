"""Null names and ids for the mt-bound SQL columns."""

from typing import TYPE_CHECKING

from dbdie_classes.options import MODEL_TYPE

if TYPE_CHECKING:
    from pandas import Series

    from dbdie_classes.base import LabelId, ModelType

ADDONS_KILLER    = "NoKillerAddon"
ADDONS_SURV      = "NoSurvAddon"
CHARACTER_ALL    = "AllCharacters"
CHARACTER_KILLER = "NoKillerCharacter"
CHARACTER_SURV   = "NoSurvCharacter"
ITEM_KILLER      = "NoKillerItem"
ITEM_SURV        = "NoSurvItem"
OFFERING_KILLER  = "NoKillerOffering"
OFFERING_SURV    = "NoSurvOffering"
PERKS_KILLER     = "NoKillerPerk"
PERKS_SURV       = "NoSurvPerk"
STATUS           = "NoStatus"

BY_MODEL_TYPE = {
    MODEL_TYPE.ADDONS    : [ADDONS_SURV, ADDONS_KILLER],
    MODEL_TYPE.CHARACTER : [CHARACTER_SURV, CHARACTER_KILLER],
    MODEL_TYPE.ITEM      : [ITEM_SURV, ITEM_KILLER],
    MODEL_TYPE.OFFERING  : [OFFERING_SURV, OFFERING_KILLER],
    MODEL_TYPE.PERKS     : [PERKS_SURV, PERKS_KILLER],
    MODEL_TYPE.STATUS    : [STATUS],
}
ALL_KILLER = [
    ADDONS_KILLER,
    CHARACTER_KILLER,
    ITEM_KILLER,
    OFFERING_KILLER,
    PERKS_KILLER,
]
ALL_SURV = [
    ADDONS_SURV,
    CHARACTER_SURV,
    ITEM_SURV,
    OFFERING_SURV,
    PERKS_SURV,
]
ALL = [
    ADDONS_KILLER,
    ADDONS_SURV,
    CHARACTER_KILLER,
    CHARACTER_SURV,
    ITEM_KILLER,
    ITEM_SURV,
    OFFERING_KILLER,
    OFFERING_SURV,
    PERKS_KILLER,
    PERKS_SURV,
    STATUS,
]

INT_IDS: dict["ModelType", list["LabelId"]] = {
    MODEL_TYPE.ADDONS    : [1, 0],  # surv, killer
    MODEL_TYPE.CHARACTER : [2, 1, 0],  # surv, killer, all
    MODEL_TYPE.ITEM      : [1, 0],
    MODEL_TYPE.OFFERING  : [1, 0],
    MODEL_TYPE.PERKS     : [1, 0],
    MODEL_TYPE.STATUS    : [0, 1],
}


def mt_is_null(data: "Series", mt: "ModelType") -> "Series":
    """Boolean mask that checks if the ModelType is null."""
    return data.isnull() | data.isin(set(INT_IDS[mt]))
