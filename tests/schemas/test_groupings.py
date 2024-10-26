"""Tests for groupings schemas."""

from copy import deepcopy
from pydantic_core import ValidationError
from pytest import mark, raises

from dbdie_classes.schemas.helpers import DBDVersionOut
from dbdie_classes.schemas.groupings import (
    FullCharacterCreate,
    PlayerIn,
)

BASE_FCC_DICT = {
    "name": "John Doe",
    "ifk": False,
    "power_name": None,
    "perk_names": ["Perk 1", "Perk 2", "Perk 3"],
    "addon_names": None,
    "dbdv": DBDVersionOut(
        id=311,
        name="7.5.0",
        common_name="Alan Wake",
        release_date="2024-01-30",
    ),
    "common_name": "John",
    "emoji": "🤠",
}


class TestGroupings:
    def test_fcc(self):
        character = FullCharacterCreate(**BASE_FCC_DICT)
        for k, v in BASE_FCC_DICT.items():
            assert getattr(character, k) == v

    def test_fcc_perk_names(self):
        d = deepcopy(BASE_FCC_DICT)

        for ifk in [False, True]:
            d["ifk"] = ifk
            d["power_name"] = "Scary lightning" if ifk else None
            d["addon_names"] = (
                [f"Addon {i}" for i in range(20)] if ifk else None
            )
            d["perk_names"] = ["Perk 1", "Perk 2", "Perk 3"]
            FullCharacterCreate(**d)

    @mark.parametrize(
        "perk_names",
        [
            [],
            ["Perk 1"],
            ["Perk 1", "Perk 2"],
            ["Perk 1", "Perk 2", "Perk 1"],
            ["Perk 1", "Perk 2", "Perk 3", "Perk 4"],
        ],
    )
    def test_fcc_perk_names_raises(self, perk_names):
        d = deepcopy(BASE_FCC_DICT)

        for ifk in [False, True]:
            d["ifk"] = ifk
            d["power_name"] = "Scary lightning" if ifk else None
            d["addon_names"] = (
                [f"Addon {i}" for i in range(20)] if ifk else None
            )
            d["perk_names"] = perk_names
            with raises(ValidationError):
                FullCharacterCreate(**d)

    def test_fcc_emoji(self):
        d = deepcopy(BASE_FCC_DICT)
        for e in ["🤠🤠", "🤠🤠🤠", 3 * "🤠"]:
            d["emoji"] = e
            FullCharacterCreate(**d)

    def test_fcc_emoji_raises(self):
        d = deepcopy(BASE_FCC_DICT)
        for e in ["", "🤠🤠🤠🤠🤠", "🤠🤠🤠🤠🤠🤠🤠", 5 * "🤠"]:
            d["emoji"] = e
            with raises(ValidationError):
                FullCharacterCreate(**d)

    def test_fcc_power_name_raises(self):
        d = deepcopy(BASE_FCC_DICT)

        d["ifk"] = True
        d["addon_names"] = [f"Addon {i}" for i in range(20)]

        with raises(ValidationError):
            FullCharacterCreate(**d)
        d["power_name"] = "Scary lightning"
        FullCharacterCreate(**d)

        d["ifk"] = False
        d["addon_names"] = None

        d["power_name"] = "Scary lightning"
        with raises(ValidationError):
            FullCharacterCreate(**d)
        d["power_name"] = None
        FullCharacterCreate(**d)

    def test_fcc_total_addons_raises(self):
        d = deepcopy(BASE_FCC_DICT)

        d["ifk"] = True
        d["power_name"] = "Scary lightning"

        with raises(ValidationError):
            FullCharacterCreate(**d)
        d["addon_names"] = [f"Addon {i}" for i in range(10)]
        with raises(ValidationError):
            FullCharacterCreate(**d)
        d["addon_names"] = [f"Addon {i}" for i in range(20)]
        FullCharacterCreate(**d)

        d["ifk"] = False
        d["power_name"] = None
        
        with raises(ValidationError):
            FullCharacterCreate(**d)
        d["addon_names"] = None
        FullCharacterCreate(**d)


    def test_player_in_count_ids(self):
        PlayerIn(
            id=0,
            character_id=None,
            perk_ids=None,
            item_id=None,
            addon_ids=None,
            offering_id=None,
            status_id=None,
            points=None,
            prestige=None,
        )
        PlayerIn(
            id=0,
            character_id=0,
            perk_ids=[0, 1, 2, 3],
            item_id=0,
            addon_ids=[0, 1],
            offering_id=0,
            status_id=0,
            points=0,
            prestige=0,
        )


    def test_player_in_count_ids_raises(self):
        with raises(ValidationError):
            PlayerIn(
                id=0,
                character_id=0,
                perk_ids=0,
                item_id=0,
                addon_ids=0,
                offering_id=0,
                status_id=0,
                points=0,
                prestige=0,
            )
        with raises(ValidationError):
            PlayerIn(
                id=0,
                character_id=0,
                perk_ids=[0, 1],
                item_id=0,
                addon_ids=[0, 1],
                offering_id=0,
                status_id=0,
                points=0,
                prestige=0,
            )
        with raises(ValidationError):
            PlayerIn(
                id=0,
                character_id=0,
                perk_ids=[0, 1, 2, 3],
                item_id=0,
                addon_ids=[0, 1, 2],
                offering_id=0,
                status_id=0,
                points=0,
                prestige=0,
            )
