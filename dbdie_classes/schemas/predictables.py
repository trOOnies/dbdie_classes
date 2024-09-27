"""Pydantic schemas for the classes that are to be predicted."""

from pydantic import BaseModel, ConfigDict, field_validator

from dbdie_classes.base import Probability


class ItemCreate(BaseModel):
    """Match item creation schema."""

    name            : str
    type_id         : int
    dbd_version_str : str | None = None
    rarity_id       : int | None = None


class ItemOut(BaseModel):
    """Match item output schema."""

    model_config = ConfigDict(from_attributes=True)

    id             : int
    name           : str
    proba          : Probability | None = None
    type_id        : int
    dbd_version_id : int | None
    rarity_id      : int | None


class AddonCreate(BaseModel):
    """Item-or-power addon creation schema."""

    name            : str
    type_id         : int
    dbd_version_str : str | None = None
    item_id         : int | None = None
    rarity_id       : int | None = None


class AddonOut(BaseModel):
    """Item-or-power addon output schema."""

    model_config = ConfigDict(from_attributes=True)

    id              : int
    name            : str
    proba           : Probability | None = None
    type_id         : int
    dbd_version_id  : int | None
    item_id         : int | None
    rarity_id       : int | None


class CharacterCreate(BaseModel):
    """Character creation schema."""

    name            : str
    is_killer       : bool | None
    base_char_id    : int | None = None  # Support for legendary outfits
    dbd_version_str : str | None = None
    common_name     : str | None = None
    emoji           : str | None = None
    power_id        : int | None = None

    @field_validator("emoji")
    @classmethod
    def emoji_len_le_4(cls, emoji: str) -> str:
        assert len(emoji) <= 4, "Emoji character-equivalence must be as most 4"
        return emoji


class CharacterOut(BaseModel):
    """Character output schema."""

    model_config = ConfigDict(from_attributes=True)

    id             : int
    name           : str
    proba          : Probability | None = None
    is_killer      : bool | None
    base_char_id   : int | None
    dbd_version_id : int | None
    common_name    : str | None
    emoji          : str | None
    power_id       : int | None


class PerkCreate(BaseModel):
    """Perk creation schema."""

    name            : str
    character_id    : int
    dbd_version_str : str | None = None
    emoji           : str | None = None

    @field_validator("emoji")
    @classmethod
    def emoji_len_le_4(cls, emoji: str) -> str:
        assert len(emoji) <= 4, "Emoji character-equivalence must be as most 4"
        return emoji


class PerkOut(BaseModel):
    """Perk output schema."""

    model_config = ConfigDict(from_attributes=True)

    id             : int
    name           : str
    proba          : Probability | None = None
    character_id   : int
    dbd_version_id : int | None
    emoji          : str | None


class OfferingCreate(BaseModel):
    """Offering creation schema."""

    model_config = ConfigDict(from_attributes=True)

    name            : str
    type_id         : int
    user_id         : int
    dbd_version_str : str | None = None
    rarity_id       : int | None = None


class OfferingOut(BaseModel):
    """Offering output schema."""

    model_config = ConfigDict(from_attributes=True)

    id             : int
    name           : str
    proba          : Probability | None = None
    type_id        : int
    user_id        : int
    dbd_version_id : int | None
    rarity_id      : int | None


class StatusCreate(BaseModel):
    """Final player match status creation schema."""

    model_config = ConfigDict(from_attributes=True)

    name            : str
    character_id    : int
    dbd_version_str : str | None = None
    emoji           : str | None = None

    @field_validator("emoji")
    @classmethod
    def emoji_len_le_4(cls, emoji: str) -> str:
        assert len(emoji) <= 4, "Emoji character-equivalence must be as most 4"
        return emoji


class StatusOut(BaseModel):
    """Final player match status output schema."""

    model_config = ConfigDict(from_attributes=True)

    id             : int
    name           : str
    proba          : Probability | None = None
    character_id   : int
    is_dead        : bool | None
    dbd_version_id : int | None
    emoji          : str | None
