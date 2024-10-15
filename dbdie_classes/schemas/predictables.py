"""Pydantic schemas for the classes that are to be predicted."""

from pydantic import BaseModel, ConfigDict, field_validator

from dbdie_classes.base import Emoji, IsForKiller, LabelId, LabelName
from dbdie_classes.code.predictables import emoji_len_func


class ItemCreate(BaseModel):
    """Match item creation schema."""

    name      : LabelName
    type_id   : int
    dbdv_id   : str | None
    rarity_id : int | None


class ItemOut(ItemCreate):
    """Match item output schema."""

    id: LabelId
    model_config = ConfigDict(from_attributes=True)


class AddonCreate(BaseModel):
    """Item-or-power addon creation schema."""

    name      : LabelName
    type_id   :     int
    dbdv_id   :     int | None
    item_id   : LabelId | None
    rarity_id :     int | None


class AddonOut(AddonCreate):
    """Item-or-power addon output schema."""

    id: LabelId
    model_config = ConfigDict(from_attributes=True)


class CharacterCreate(BaseModel):
    """Character creation schema."""

    name         : LabelName
    ifk          : IsForKiller
    base_char_id : LabelId | None  # Support for legendary outfits
    dbdv_id      :     int | None
    common_name  :     str | None
    emoji        :   Emoji | None
    power_id     : LabelId | None

    @field_validator("emoji")
    @classmethod
    def emoji_len(cls, emoji: Emoji | None) -> Emoji | None:
        return emoji_len_func(emoji)


class CharacterOut(CharacterCreate): 
    """Character output schema."""

    id: LabelId
    model_config = ConfigDict(from_attributes=True)


class PerkCreate(BaseModel):
    """Perk creation schema."""

    name         : LabelName
    character_id : LabelId
    dbdv_id      :     int | None
    emoji        :   Emoji | None

    @field_validator("emoji")
    @classmethod
    def emoji_len(cls, emoji: Emoji | None) -> Emoji | None:
        return emoji_len_func(emoji)


class PerkOut(PerkCreate):
    """Perk output schema."""

    id: LabelId
    model_config = ConfigDict(from_attributes=True)


class OfferingCreate(BaseModel):
    """Offering creation schema."""

    name      : LabelName
    type_id   : int
    user_id   : LabelId
    dbdv_id   : int | None
    rarity_id : int | None


class OfferingOut(OfferingCreate):
    """Offering output schema."""

    id: LabelId
    model_config = ConfigDict(from_attributes=True)


class StatusCreate(BaseModel):
    """Final player match status creation schema."""

    name         : LabelName
    character_id :   LabelId
    is_dead      :      bool | None
    dbdv_id      :       int | None
    emoji        :     Emoji | None

    @field_validator("emoji")
    @classmethod
    def emoji_len(cls, emoji: Emoji | None) -> Emoji | None:
        return emoji_len_func(emoji)


class StatusOut(StatusCreate):
    """Final player match status output schema."""

    id: LabelId
    model_config = ConfigDict(from_attributes=True)
