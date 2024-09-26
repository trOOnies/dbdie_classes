"""Pydantic schemas for the predictables' types."""

from pydantic import BaseModel, field_validator


class ItemTypeOut(BaseModel):
    """Match item type output schema."""
    id            : int
    name          : str
    emoji         : str | None
    is_for_killer : bool | None


class AddonTypeOut(BaseModel):
    """Item-or-power addon type output schema."""
    id            : int
    name          : str
    emoji         : str | None
    is_for_killer : bool | None


class OfferingTypeOut(BaseModel):
    """Offering type output schema."""
    id            : int
    name          : str
    emoji         : str | None
    is_for_killer : bool | None


class RarityCreate(BaseModel):
    """Item rarity create schema."""
    name: str
    color: str
    emoji: str

    @field_validator("emoji")
    @classmethod
    def emoji_len_le_4(cls, emoji: str) -> str:
        assert len(emoji) <= 4, "Emoji character-equivalence must be as most 4"
        return emoji


class RarityOut(BaseModel):
    """Item rarity output schema."""
    id: int
    name: str
    color: str
    emoji: str
