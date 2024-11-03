"""Pydantic schemas for the classes that are to be predicted."""

from pydantic import BaseModel, ConfigDict, Field, field_validator

from dbdie_classes.base import Emoji, IsForKiller, LabelId, LabelName
from dbdie_classes.code.predictables import emoji_len_func


class ItemCreate(BaseModel):
    """Match item creation schema."""

    name      : LabelName  = Field(..., description="Item's name")
    type_id   : int        = Field(..., description="Item's type ID")
    dbdv_id   : str | None = Field(..., description="Item's release DBD version id")
    rarity_id : int | None = Field(..., description="Item's rarity ID")


class ItemOut(ItemCreate):
    """Match item output schema."""

    id: LabelId  = Field(..., description="Item's ID")
    model_config = ConfigDict(from_attributes=True)


class AddonCreate(BaseModel):
    """Item-or-power addon creation schema."""

    name      : LabelName        = Field(..., description="Addon's name")
    type_id   :       int        = Field(..., description="Addon's type ID")
    dbdv_id   :       int | None = Field(..., description="Addon's release DBD version id")
    item_id   :   LabelId | None = Field(..., description="Addon's item ID")
    rarity_id :       int | None = Field(..., description="Addon's rarity ID")


class AddonOut(AddonCreate):
    """Item-or-power addon output schema."""

    id: LabelId  = Field(..., description="Addon's ID")
    model_config = ConfigDict(from_attributes=True)


class CharacterCreate(BaseModel):
    """Character creation schema."""

    name         : LabelName      = Field(..., description="Character's name")
    ifk          : IsForKiller    = Field(..., description="Is for Killer")
    base_char_id : LabelId | None = Field(..., description="Base character ID (used for legendary outfits)")
    dbdv_id      :     int | None = Field(..., description="Character's release DBD version id")
    common_name  :     str | None = Field(..., description="Character's common name")
    emoji        :   Emoji | None = Field(..., description="Character's corresponding emoji")
    power_id     : LabelId | None = Field(..., description="Character's power ID")

    @field_validator("emoji")
    @classmethod
    def emoji_len(cls, emoji: Emoji | None) -> Emoji | None:
        return emoji_len_func(emoji)


class CharacterOut(CharacterCreate): 
    """Character output schema."""

    id: LabelId  = Field(..., description="Character's ID")
    model_config = ConfigDict(from_attributes=True)


class PerkCreate(BaseModel):
    """Perk creation schema."""

    name         : LabelName      = Field(..., description="Perk's name")
    character_id : LabelId        = Field(..., description="ID of the perk's character")
    dbdv_id      :     int | None = Field(..., description="Perk's release DBD version id")
    emoji        :   Emoji | None = Field(..., description="Perk's corresponding emoji")

    @field_validator("emoji")
    @classmethod
    def emoji_len(cls, emoji: Emoji | None) -> Emoji | None:
        return emoji_len_func(emoji)


class PerkOut(PerkCreate):
    """Perk output schema."""

    id: LabelId  = Field(..., description="Perk's ID")
    model_config = ConfigDict(from_attributes=True)


class OfferingCreate(BaseModel):
    """Offering creation schema."""

    name      : LabelName  = Field(..., description="Offering's name")
    type_id   : int        = Field(..., description="Offering's type ID")
    user_id   : LabelId    = Field(..., description="Offering's special user ID (all, killer or survivor)")
    dbdv_id   : int | None = Field(..., description="Offering's release DBD version id")
    rarity_id : int | None = Field(..., description="Offering's rarity ID")


class OfferingOut(OfferingCreate):
    """Offering output schema."""

    id: LabelId  = Field(..., description="Offering's ID")
    model_config = ConfigDict(from_attributes=True)


class StatusCreate(BaseModel):
    """Final player match status creation schema."""

    name         : LabelName        = Field(..., description="Status' name")
    character_id :   LabelId        = Field(..., description="Character special ID (killer or survivor)")
    is_dead      :      bool | None = Field(..., description="Whether the player is dead")
    dbdv_id      :       int | None = Field(..., description="Status' release DBD version id")
    emoji        :     Emoji | None = Field(..., description="Status' corresponding emoji")

    @field_validator("emoji")
    @classmethod
    def emoji_len(cls, emoji: Emoji | None) -> Emoji | None:
        return emoji_len_func(emoji)


class StatusOut(StatusCreate):
    """Final player match status output schema."""

    id: LabelId  = Field(..., description="Status's ID")
    model_config = ConfigDict(from_attributes=True)
