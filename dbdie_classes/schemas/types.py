"""Pydantic schemas for the predictables' types."""

from pydantic import BaseModel, ConfigDict, Field, field_validator

from dbdie_classes.base import Emoji, IsForKiller
from dbdie_classes.code.predictables import emoji_len_func


class ItemTypeCreate(BaseModel):
    """Match item type create schema."""
    name  : str          = Field(..., description="Item type name")
    emoji : Emoji | None = Field(..., description="Item type corresponding emoji")
    ifk   : IsForKiller  = Field(..., description="Is for Killer")


class ItemTypeOut(ItemTypeCreate):
    """Match item type output schema."""
    id: int      = Field(..., description="Item type ID")
    model_config = ConfigDict(from_attributes=True)


class AddonTypeCreate(BaseModel):
    """Item-or-power addon type create schema."""
    name  : str          = Field(..., description="Addon type name")
    emoji : Emoji | None = Field(..., description="Addon type corresponding emoji")
    ifk   : IsForKiller  = Field(..., description="Is for Killer")


class AddonTypeOut(AddonTypeCreate):
    """Item-or-power addon type output schema."""
    id:      int = Field(..., description="Addon type ID")
    model_config = ConfigDict(from_attributes=True)


class OfferingTypeCreate(BaseModel):
    """Offering type create schema."""
    name  : str          = Field(..., description="Offering type name")
    emoji : Emoji | None = Field(..., description="Offering type corresponding emoji")
    ifk   : IsForKiller  = Field(..., description="Is for Killer")


class OfferingTypeOut(OfferingTypeCreate):
    """Offering type output schema."""
    id: int      = Field(..., description="Offering type ID")
    model_config = ConfigDict(from_attributes=True)


class RarityCreate(BaseModel):
    """Item rarity create schema."""
    name  : str   = Field(..., description="Rarity name")
    color : str   = Field(..., description="Rarity color")
    emoji : Emoji = Field(..., description="Rarity corresponding emoji")

    @field_validator("emoji")
    @classmethod
    def emoji_len(cls, emoji: Emoji | None) -> Emoji | None:
        return emoji_len_func(emoji)


class RarityOut(RarityCreate):
    """Item rarity output schema."""
    id: int      = Field(..., description="Rarity ID")
    model_config = ConfigDict(from_attributes=True)
