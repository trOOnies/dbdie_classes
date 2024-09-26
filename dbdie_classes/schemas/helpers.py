"""Pydantic schemas for the helper classes."""

import datetime as dt
from pydantic import BaseModel


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
