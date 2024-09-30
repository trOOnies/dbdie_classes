"""Pydantic schemas for class objects related to DBDIE."""

from __future__ import annotations

import datetime as dt
from pydantic import BaseModel, Field

TOTAL_VALID_FMTS = 13


class UserCreate(BaseModel):
    """DBDIE user create schema."""

    name: str


class UserOut(BaseModel):
    """DBDIE user output schema."""

    id: int
    name: str


class CropperSwarmCreate(BaseModel):
    """DBDIE CropperSwarm create schema."""

    name:          str
    user_id:       int
    img_width:     int
    img_height:    int
    dbdv_min_id:   int
    dbdv_max_id:   int | None
    is_for_killer: bool | None


class CropperSwarmOut(BaseModel):
    """DBDIE CropperSwarm output schema."""

    id:            int
    name:          str
    user_id:       int
    img_width:     int
    img_height:    int
    dbdv_min_id:   int
    dbdv_max_id:   int | None
    is_for_killer: bool | None


class FullModelTypeCreate(BaseModel):
    """DBDIE full model type create schema."""

    name:          str
    model_type:    str
    is_for_killer: bool | None


class FullModelTypeOut(BaseModel):
    """DBDIE full model type output schema."""

    id:            int
    name:          str
    model_type:    str
    is_for_killer: bool | None


class ModelCreate(BaseModel):
    """DBDIE IEModel create schema."""

    name:              str
    user_id:           int
    fmt_id:            int  # TODO: ?
    cropper_swarm_id:  int
    dbdv_min_id:       int
    dbdv_max_id:       int | None
    special_mode:      bool | None = None
    date_created:      str | None = None
    date_modified:     str | None = None
    date_last_trained: str | None

    def model_post_init(self, __context) -> None:
        if self.date_last_trained is None:
            self.date_last_trained = dt.date.today().strftime("%Y-%m-%d")


class ModelOut(BaseModel):
    """DBDIE IEModel output schema."""

    id:                  int
    name:                str
    user_id:             int
    fmt_id:              int  # TODO: ?
    cropper_swarm_id:    int
    dbdv_min_id:         int
    dbdv_max_id:         int | None
    special_mode:        bool | None
    date_created:        dt.datetime
    date_modified:       dt.datetime
    date_last_trained:   dt.date


class ExtractorModelsIds(BaseModel):
    """Ids of the IEModels of an InfoExtractor."""

    mid_0:  int | None = Field(None, ge=0)
    mid_1:  int | None = Field(None, ge=0)
    mid_2:  int | None = Field(None, ge=0)
    mid_3:  int | None = Field(None, ge=0)
    mid_4:  int | None = Field(None, ge=0)
    mid_5:  int | None = Field(None, ge=0)
    mid_6:  int | None = Field(None, ge=0)
    mid_7:  int | None = Field(None, ge=0)
    mid_8:  int | None = Field(None, ge=0)
    mid_9:  int | None = Field(None, ge=0)
    mid_10: int | None = Field(None, ge=0)
    mid_11: int | None = Field(None, ge=0)
    mid_12: int | None = Field(None, ge=0)

    @property
    def ids(self) -> list[int | None]:
        return [
            self.mid_0,
            self.mid_1,
            self.mid_2,
            self.mid_3,
            self.mid_4,
            self.mid_5,
            self.mid_6,
            self.mid_7,
            self.mid_8,
            self.mid_9,
            self.mid_10,
            self.mid_11,
            self.mid_12,
        ]

    def any(self) -> bool:
        return any(mid is not None for mid in self.ids)

    def all(self) -> bool:
        return all(mid is not None for mid in self.ids)

    def to_sql_cols(self) -> dict:
        return {f"mid_{i}": mid for i, mid in enumerate(self.ids)}


class ExtractorCreate(BaseModel):
    """DBDIE InfoExtractor create schema."""

    name:                str
    user_id:             int
    dbdv_min_id:         int
    dbdv_max_id:         int | None
    special_mode:        bool | None = None
    cropper_swarm_id:    int
    models_ids:          ExtractorModelsIds
    date_created:        str | None = None
    date_modified:       str | None = None
    date_last_trained:   str | None

    def model_post_init(self, __context) -> None:
        assert self.models_ids.any()
        if self.date_last_trained is None:
            self.date_last_trained = dt.date.today().strftime("%Y-%m-%d")


class ExtractorOut(BaseModel):
    """DBDIE InfoExtractor output schema."""

    id:                  int
    name:                str
    user_id:             int
    dbdv_min_id:         int
    dbdv_max_id:         int | None
    special_mode:        bool | None
    cropper_swarm_id:    int
    models_ids:          ExtractorModelsIds
    date_created:        dt.datetime
    date_modified:       dt.datetime
    date_last_trained:   dt.date

    @classmethod
    def from_sqla(cls, extractor) -> ExtractorOut:
        return ExtractorOut(
            id=extractor.id,
            name=extractor.name,
            user_id=extractor.user_id,
            dbdv_min_id=extractor.dbdv_min_id,
            dbdv_max_id=extractor.dbdv_max_id,
            special_mode=extractor.special_mode,
            cropper_swarm_id=extractor.cropper_swarm_id,
            models_ids={
                f"mid_{i}": getattr(extractor, f"mid_{i}")
                for i in range(TOTAL_VALID_FMTS)
            },
            date_created=extractor.date_created,
            date_modified=extractor.date_modified,
            date_last_trained=extractor.date_last_trained,
        )
