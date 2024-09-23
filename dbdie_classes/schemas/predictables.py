"""Pydantic schemas for the classes that are to be predicted."""

import datetime as dt

from pydantic import BaseModel, ConfigDict

from dbdie_classes.base import Probability


class DBDVersionCreate(BaseModel):
    """DBD game version creation schema."""

    name         : str
    release_date : dt.date | None


class DBDVersionOut(BaseModel):
    """DBD game version output schema."""

    id           : int
    name         : str
    common_name  : str | None
    release_date : dt.date | None


class CharacterCreate(BaseModel):
    """Character creation schema."""

    name            : str
    is_killer       : bool | None
    base_char_id    : int | None = None  # Support for legendary outfits
    dbd_version_str : str | None = None
    emoji           : str | None = None


class CharacterOut(BaseModel):
    """Character output schema."""

    model_config = ConfigDict(from_attributes=True)

    id             : int
    name           : str
    common_name    : str | None
    proba          : Probability | None = None
    is_killer      : bool | None
    base_char_id   : int | None
    dbd_version_id : int | None
    emoji          : str | None


class PerkCreate(BaseModel):
    """Perk creation schema."""

    name            : str
    character_id    : int
    dbd_version_str : str | None = None
    emoji           : str | None = None


class PerkOut(BaseModel):
    """Perk output schema."""

    model_config = ConfigDict(from_attributes=True)

    id             : int
    name           : str
    proba          : Probability | None = None
    character_id   : int
    is_for_killer  : bool | None
    dbd_version_id : int | None
    emoji          : str | None


class ItemCreate(BaseModel):
    """Match item creation schema."""

    name    : str
    type_id : int


class ItemOut(BaseModel):
    """Match item output schema."""

    model_config = ConfigDict(from_attributes=True)

    id      : int
    name    : str
    proba   : Probability | None = None
    type_id : int


class ItemTypeOut(BaseModel):
    """Match item type output schema."""
    id            : int
    name          : str
    emoji         : str | None
    is_for_killer : bool | None


class OfferingCreate(BaseModel):
    """Offering creation schema."""

    model_config = ConfigDict(from_attributes=True)

    name    : str
    type_id : int
    user_id : int


class OfferingOut(BaseModel):
    """Offering output schema."""

    model_config = ConfigDict(from_attributes=True)

    id            : int
    name          : str
    proba         : Probability | None = None
    type_id       : int
    user_id       : int
    is_for_killer : bool | None


class OfferingTypeOut(BaseModel):
    """Offering type output schema."""
    id            : int
    name          : str
    emoji         : str | None
    is_for_killer : bool | None


class AddonCreate(BaseModel):
    """Item-or-power addon creation schema."""

    name            : str
    type_id         : int
    user_id         : int
    dbd_version_str : str | None = None


class AddonOut(BaseModel):
    """Item-or-power addon output schema."""

    model_config = ConfigDict(from_attributes=True)

    id             : int
    name           : str
    proba          : Probability | None = None
    type_id        : int
    user_id        : int
    dbd_version_id : int | None


class AddonTypeOut(BaseModel):
    """Item-or-power addon type output schema."""
    id            : int
    name          : str
    emoji         : str | None
    is_for_killer : bool | None


class StatusCreate(BaseModel):
    """Final player match status creation schema."""

    model_config = ConfigDict(from_attributes=True)

    name         : str
    character_id : int
    emoji        : str | None = None


class StatusOut(BaseModel):
    """Final player match status output schema."""

    model_config = ConfigDict(from_attributes=True)

    id           : int
    name         : str
    proba        : Probability | None = None
    character_id : int
    is_dead      : bool | None
    emoji        : str | None
