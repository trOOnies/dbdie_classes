"""Types of predictables that necessarily end up as different models.
They aren't 'full' (FullModelTypes) because they lack the surv / killer suffix.
"""

ADDONS    = "addons"
CHARACTER = "character"
ITEM      = "item"
OFFERING  = "offering"
PERKS     = "perks"
POINTS    = "points"
PRESTIGE  = "prestige"
STATUS    = "status"

UNIQUE_PER_PLAYER = [
    CHARACTER,
    ITEM,
    OFFERING,
    POINTS,
    PRESTIGE,
    STATUS,
]
MULTIPLE_PER_PLAYER = [
    ADDONS,
    PERKS,
]

ALL_MULTIPLE_CHOICE = [
    ADDONS,
    CHARACTER,
    ITEM,
    OFFERING,
    PERKS,
    STATUS,
]
ALL = [
    ADDONS,
    CHARACTER,
    ITEM,
    OFFERING,
    PERKS,
    POINTS,
    PRESTIGE,
    STATUS,
]
# EMOJIS = ["💡", "🧑", "🔦", "🛑", "💠", "🔢", "❇️", "💀"]
EMOJIS = ["💡", "🧑", "🔦", "🛑", "💠", "💀"]

WITH_TYPES = [ADDONS, ITEM, OFFERING]

TO_ID_NAMES = {
    ADDONS: "addon_ids",
    CHARACTER: "character_id",
    ITEM: "item_id",
    OFFERING: "offering_id",
    PERKS: "perk_ids",
    POINTS: "points",
    PRESTIGE: "prestige",
    STATUS: "status_id",
}
