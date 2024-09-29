"""Types of predictables that necessarily end up as different models.
They aren't 'full' (FullModelTypes) because they lack the surv / killer suffix.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dbdie_classes.base import Emoji, ModelType

ADDONS    : "ModelType" = "addons"
CHARACTER : "ModelType" = "character"
ITEM      : "ModelType" = "item"
OFFERING  : "ModelType" = "offering"
PERKS     : "ModelType" = "perks"
POINTS    : "ModelType" = "points"
PRESTIGE  : "ModelType" = "prestige"
STATUS    : "ModelType" = "status"

UNIQUE_PER_PLAYER: list["ModelType"] = [
    CHARACTER,
    ITEM,
    OFFERING,
    POINTS,
    PRESTIGE,
    STATUS,
]
MULTIPLE_PER_PLAYER: list["ModelType"] = [
    ADDONS,
    PERKS,
]

ALL_MULTIPLE_CHOICE: list["ModelType"] = [
    ADDONS,
    CHARACTER,
    ITEM,
    OFFERING,
    PERKS,
    STATUS,
]
ALL: list["ModelType"] = [
    ADDONS,
    CHARACTER,
    ITEM,
    OFFERING,
    PERKS,
    POINTS,
    PRESTIGE,
    STATUS,
]
# EMOJIS: list["Emoji"] = ["💡", "🧑", "🔦", "🛑", "💠", "🔢", "❇️", "💀"]
EMOJIS: list["Emoji"] = ["💡", "🧑", "🔦", "🛑", "💠", "💀"]

WITH_TYPES: list["ModelType"] = [ADDONS, ITEM, OFFERING]

TO_ID_NAMES: dict["ModelType", str] = {
    ADDONS: "addon_ids",
    CHARACTER: "character_id",
    ITEM: "item_id",
    OFFERING: "offering_id",
    PERKS: "perk_ids",
    POINTS: "points",
    PRESTIGE: "prestige",
    STATUS: "status_id",
}
