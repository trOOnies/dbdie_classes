"""Pydantic schemas for the predictables' types."""

from pydantic import BaseModel, ConfigDict, field_validator

from dbdie_classes.base import Emoji, IsForKiller


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
    def emoji_len(cls, emoji: str) -> Emoji:
        assert len(emoji) == 1, "The emoji attribute can only be 1 character."
        return emoji


class RarityOut(RarityCreate):
    """Item rarity output schema."""
    id: int
    model_config = ConfigDict(from_attributes=True)
