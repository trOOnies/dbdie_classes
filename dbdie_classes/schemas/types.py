"""Pydantic schemas for the predictables' types."""

from pydantic import BaseModel, field_validator

from dbdie_classes.base import Emoji, IsForKiller


class ItemTypeOut(BaseModel):
    """Match item type output schema."""
    id            :   int
    name          :   str
    emoji         : Emoji | None
    ifk           :  IsForKiller


class AddonTypeOut(BaseModel):
    """Item-or-power addon type output schema."""
    id            :   int
    name          :   str
    emoji         : Emoji | None
    ifk           :  IsForKiller


class OfferingTypeOut(BaseModel):
    """Offering type output schema."""
    id            :   int
    name          :   str
    emoji         : Emoji | None
    ifk           :  IsForKiller


class RarityCreate(BaseModel):
    """Item rarity create schema."""
    name:  str
    color: str
    emoji: Emoji

    @field_validator("emoji")
    @classmethod
    def emoji_len(cls, emoji: str) -> Emoji:
        assert len(emoji) == 1, "The emoji attribute can only be 1 character."
        return emoji


class RarityOut(BaseModel):
    """Item rarity output schema."""
    id:    int
    name:  str
    color: str
    emoji: Emoji
