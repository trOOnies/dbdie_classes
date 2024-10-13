"""Tests for groupings schemas."""

from copy import deepcopy
from pydantic_core import ValidationError
from pytest import raises

from dbdie_classes.schemas.helpers import DBDVersionOut
from dbdie_classes.schemas.groupings import FullCharacterCreate

BASE_FCC_DICT = {
    "name": "John Doe",
    "ifk": False,
    "power_name": None,
    "perk_names": ["Perk 1", "Perk 2", "Perk 3"],
    "addon_names": None,
    "dbd_version": DBDVersionOut.from_str("7.5.0"),
    "common_name": "John",
    "emoji": "🤠",
}


class TestGroupings:
    def test_fcc(self):
        character = FullCharacterCreate(**BASE_FCC_DICT)
        for k, v in BASE_FCC_DICT.items():
            assert getattr(character, k) == v

    def test_fcc_perk_names_raises(self):
        d = deepcopy(BASE_FCC_DICT)

        for ifk in [False, True]:
            d["ifk"] = ifk
            d["power_name"] = "Scary lightning" if ifk else None
            d["addon_names"] = (
                [f"Addon {i}" for i in range(20)] if ifk else None
            )

            d["perk_names"] = []
            with raises(ValidationError):
                FullCharacterCreate(**d)
            d["perk_names"] = ["Perk 1"]
            with raises(ValidationError):
                FullCharacterCreate(**d)
            d["perk_names"] = ["Perk 1", "Perk 2"]
            with raises(ValidationError):
                FullCharacterCreate(**d)
            d["perk_names"] = ["Perk 1", "Perk 2", "Perk 3"]
            FullCharacterCreate(**d)
            d["perk_names"] = ["Perk 1", "Perk 2", "Perk 1"]
            with raises(ValidationError):
                FullCharacterCreate(**d)
            d["perk_names"] = ["Perk 1", "Perk 2", "Perk 3", "Perk 4"]
            with raises(ValidationError):
                FullCharacterCreate(**d)

    def test_fcc_emoji_raises(self):
        d = deepcopy(BASE_FCC_DICT)
        for e in ["", "🤠🤠", "🤠🤠🤠"]:
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
