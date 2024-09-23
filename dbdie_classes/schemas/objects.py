"""Pydantic schemas for class objects related to DBDIE."""

import datetime as dt
from pydantic import BaseModel, Field


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
    is_for_killer: bool


class FullModelTypeOut(BaseModel):
    """DBDIE full model type output schema."""

    id:            int
    name:          str
    model_type:    str
    is_for_killer: bool


class ModelCreate(BaseModel):
    """DBDIE IEModel create schema."""

    name:             str
    user_id:          int
    fmt_id:           int  # TODO: ?
    cropper_swarm_id: int
    dbdv_min_id:      int
    dbdv_max_id:      int | None
    special_mode:     bool | None = None
    trained:          bool


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

    addons:    int | None = Field(None, ge=0)
    character: int | None = Field(None, ge=0)
    item:      int | None = Field(None, ge=0)
    offering:  int | None = Field(None, ge=0)
    perks:     int | None = Field(None, ge=0)
    points:    int | None = Field(None, ge=0)
    prestige:  int | None = Field(None, ge=0)
    status:    int | None = Field(None, ge=0)

    def ids(self) -> list[int | None]:
        return [
            self.addons,
            self.character,
            self.item,
            self.offering,
            self.perks,
            self.points,
            self.prestige,
            self.status,
        ]

    def any(self) -> bool:
        return any(mid is not None for mid in self.ids)

    def all(self) -> bool:
        return all(mid is not None for mid in self.ids)

    def to_sql_cols(self) -> dict:
        return {
            "mid_addons": self.addons,
            "mid_character": self.character,
            "mid_item": self.item,
            "mid_offering": self.offering,
            "mid_perks": self.perks,
            "mid_points": self.points,
            "mid_prestige": self.prestige,
            "mid_status": self.status,
        }


class ExtractorCreate(BaseModel):
    """DBDIE InfoExtractor create schema."""

    name:             str
    user_id:          int
    dbdv_min_id:      int
    dbdv_max_id:      int | None
    special_mode:     bool | None = None
    cropper_swarm_id: int
    models_ids:       ExtractorModelsIds
    trained:          bool

    def model_post_init(self, __context) -> None:
        assert self.models_ids.any()


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
