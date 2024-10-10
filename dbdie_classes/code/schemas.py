"""Extra code for the schemas Python file."""

from typing import TYPE_CHECKING, Union

from dbdie_classes.options import PLAYER_TYPE as PT

if TYPE_CHECKING:
    from dbdie_classes.schemas.predictables import AddonOut, OfferingOut, PerkOut

ALL_CHARS_IDS = {"all": 0, PT.KILLER: 1, PT.SURV: 2}
ADDONS_IDS = {"none": 0, PT.KILLER: 1, "base": (2, 3, 4, 5, 6)}

# * PlayerOut


def check_killer_consistency(
    ifk: bool,
    obj: Union["OfferingOut", "PerkOut"],
) -> bool:
    return obj.ifk is None or (obj.ifk == ifk)


def check_item_consistency(ifk: bool, item_type_id: int) -> bool:
    # TODO: Decouple from addons
    return ifk == (item_type_id == ADDONS_IDS[PT.KILLER])


def check_addons_consistency(
    ifk: bool,
    addons: list["AddonOut"],
) -> bool:
    return all(
        a.type_id == ADDONS_IDS["none"]
        or ((a.type_id == ADDONS_IDS[PT.KILLER]) == ifk)
        for a in addons
    )


def check_status_consistency(
    status_character_id: int,
    ifk: bool,
) -> bool:
    return (
        status_character_id == ALL_CHARS_IDS["all"]
        or ((status_character_id == ALL_CHARS_IDS[PT.SURV]) == (not ifk))
        or ((status_character_id == ALL_CHARS_IDS[PT.KILLER]) == ifk)
    )
