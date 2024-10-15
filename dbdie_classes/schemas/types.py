"""Pydantic schemas for the predictables' types."""

from pydantic import BaseModel, ConfigDict, field_validator

from dbdie_classes.base import Emoji, IsForKiller
from dbdie_classes.code.predictables import emoji_len_func


class ItemTypeCreate(BaseModel):
    """Match item type create schema."""
    name  : str
    emoji : Emoji | None
    ifk   : IsForKiller


class ItemTypeOut(ItemTypeCreate):
    """Match item type output schema."""
    id: int
    model_config = ConfigDict(from_attributes=True)


class AddonTypeCreate(BaseModel):
    """Item-or-power addon type create schema."""
    name  : str
    emoji : Emoji | None
    ifk   : IsForKiller


class AddonTypeOut(AddonTypeCreate):
    """Item-or-power addon type output schema."""
    id: int
    model_config = ConfigDict(from_attributes=True)


class OfferingTypeCreate(BaseModel):
    """Offering type create schema."""
    name  : str
    emoji : Emoji | None
    ifk   : IsForKiller


class OfferingTypeOut(OfferingTypeCreate):
    """Offering type output schema."""
    id: int
    model_config = ConfigDict(from_attributes=True)


class RarityCreate(BaseModel):
    """Item rarity create schema."""
    name  :  str
    color : str
    emoji : Emoji

    @field_validator("emoji")
    @classmethod
    def emoji_len(cls, emoji: Emoji | None) -> Emoji | None:
        return emoji_len_func(emoji)


class RarityOut(RarityCreate):
    """Item rarity output schema."""
    id: int
    model_config = ConfigDict(from_attributes=True)
