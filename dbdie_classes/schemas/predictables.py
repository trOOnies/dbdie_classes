"""Pydantic schemas for the classes that are to be predicted."""

from pydantic import BaseModel, ConfigDict, field_validator

from dbdie_classes.base import Emoji, IsForKiller, LabelId, LabelName, Probability


class ItemCreate(BaseModel):
    """Match item creation schema."""

    name            : LabelName
    type_id         : int
    dbd_version_str : str | None = None
    rarity_id       : int | None = None


class ItemOut(BaseModel):
    """Match item output schema."""

    model_config = ConfigDict(from_attributes=True)

    id             : LabelId
    name           : LabelName
    type_id        : int
    dbd_version_id : int | None
    rarity_id      : int | None
    proba          : Probability | None = None


class AddonCreate(BaseModel):
    """Item-or-power addon creation schema."""

    name            : LabelName
    type_id         :     int
    dbd_version_str :     str | None = None
    item_id         : LabelId | None = None
    rarity_id       :     int | None = None


class AddonOut(BaseModel):
    """Item-or-power addon output schema."""

    model_config = ConfigDict(from_attributes=True)

    id              : LabelId
    name            : LabelName
    type_id         :     int
    dbd_version_id  :     int | None
    item_id         : LabelId | None
    rarity_id       :     int | None
    proba           : Probability | None = None


class CharacterCreate(BaseModel):
    """Character creation schema."""

    name            : LabelName
    is_killer       : IsForKiller
    base_char_id    : LabelId | None = None  # Support for legendary outfits
    dbd_version_str :     str | None = None
    common_name     :     str | None = None
    emoji           :   Emoji | None = None
    power_id        : LabelId | None = None

    @field_validator("emoji")
    @classmethod
    def emoji_len(cls, emoji: str) -> Emoji:
        assert len(emoji) == 1, "The emoji attribute can only be 1 character."
        return emoji


class CharacterOut(BaseModel):
    """Character output schema."""

    model_config = ConfigDict(from_attributes=True)

    id             : LabelId
    name           : LabelName
    is_killer      : IsForKiller
    base_char_id   : LabelId | None
    dbd_version_id :     int | None
    common_name    :     str | None
    emoji          :   Emoji | None
    power_id       : LabelId | None
    proba          : Probability | None = None


class PerkCreate(BaseModel):
    """Perk creation schema."""

    name            : LabelName
    character_id    : LabelId
    dbd_version_str :     str | None = None
    emoji           :   Emoji | None = None

    @field_validator("emoji")
    @classmethod
    def emoji_len(cls, emoji: str) -> Emoji:
        assert len(emoji) == 1, "The emoji attribute can only be 1 character."
        return emoji


class PerkOut(BaseModel):
    """Perk output schema."""

    model_config = ConfigDict(from_attributes=True)

    id             : LabelId
    name           : LabelName
    character_id   : LabelId
    dbd_version_id :     int | None
    emoji          :   Emoji | None
    proba          : Probability | None = None


class OfferingCreate(BaseModel):
    """Offering creation schema."""

    model_config = ConfigDict(from_attributes=True)

    name            : LabelName
    type_id         : int
    user_id         : LabelId
    dbd_version_str : str | None = None
    rarity_id       : int | None = None


class OfferingOut(BaseModel):
    """Offering output schema."""

    model_config = ConfigDict(from_attributes=True)

    id             : LabelId
    name           : LabelName
    type_id        : int
    user_id        : LabelId
    dbd_version_id : int | None
    rarity_id      : int | None
    proba          : Probability | None = None


class StatusCreate(BaseModel):
    """Final player match status creation schema."""

    model_config = ConfigDict(from_attributes=True)

    name            : LabelName
    character_id    : LabelId
    dbd_version_str :     str | None = None
    emoji           :   Emoji | None = None

    @field_validator("emoji")
    @classmethod
    def emoji_len(cls, emoji: str) -> Emoji:
        assert len(emoji) == 1, "The emoji attribute can only be 1 character."
        return emoji


class StatusOut(BaseModel):
    """Final player match status output schema."""

    model_config = ConfigDict(from_attributes=True)

    id             : LabelId
    name           : LabelName
    character_id   : LabelId
    is_dead        :    bool | None
    dbd_version_id :     int | None
    emoji          :   Emoji | None
    proba          : Probability | None = None
