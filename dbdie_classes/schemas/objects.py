"""Pydantic schemas for class objects related to DBDIE."""

from __future__ import annotations

import datetime as dt
from pydantic import BaseModel, ConfigDict, Field
from typing import TYPE_CHECKING

from dbdie_classes.options.FMT import ALL as ALL_FMT

if TYPE_CHECKING:
    from dbdie_classes.base import FullModelType

TOTAL_VALID_FMTS = len(ALL_FMT)


class UserCreate(BaseModel):
    """DBDIE user create schema."""

    name: str


class UserOut(UserCreate):
    """DBDIE user output schema."""

    id: int
    model_config = ConfigDict(from_attributes=True)


class CropperSwarmCreate(BaseModel):
    """DBDIE `CropperSwarm` register entry create schema."""

    name:          str
    user_id:       int
    img_width:     int
    img_height:    int
    dbdv_min_id:   int
    dbdv_max_id:   int | None
    ifk:           bool | None


class CropperSwarmOut(CropperSwarmCreate):
    """DBDIE `CropperSwarm` register entry output schema."""

    id: int
    model_config = ConfigDict(from_attributes=True)


class FullModelTypeCreate(BaseModel):
    """DBDIE full model type create schema."""

    name: str
    mt:   str
    ifk:  bool | None


class FullModelTypeOut(FullModelTypeCreate):
    """DBDIE full model type output schema."""

    id: int
    model_config = ConfigDict(from_attributes=True)


class ModelCreate(BaseModel):
    """DBDIE `IEModel` register entry create schema."""

    id:                int  # we need the ID before registering it
    name:              str
    user_id:           int
    fmt_id:            int
    cps_id:            int
    dbdv_min_id:       int
    dbdv_max_id:       int | None
    special_mode:      bool | None
    date_created:      dt.datetime
    date_modified:     dt.datetime
    date_last_trained: dt.date

    def model_post_init(self, __context) -> None:
        if self.date_last_trained is None:
            self.date_last_trained = dt.date.today().strftime("%Y-%m-%d")


class ModelOut(ModelCreate):
    """DBDIE `IEModel` register entry output schema."""

    model_config = ConfigDict(from_attributes=True)


class ExtractorModelsIds(BaseModel):
    """Ids of the `IEModels` of an `InfoExtractor`."""

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

    @classmethod
    def from_fmt_dict(cls, fmt_dict: dict["FullModelType", int]) -> ExtractorModelsIds:
        fmt_dict_ = {
            fmt: (fmt_dict[fmt] if fmt in fmt_dict else None)
            for fmt in ALL_FMT
        }
        return cls(**{f"mid_{i}": mid for i, mid in enumerate(fmt_dict_.values())})

    @classmethod
    def from_extractor(cls, extractor) -> ExtractorModelsIds:
        return cls(
            **{
                f"mid_{i}": getattr(extractor, f"mid_{i}")
                for i in range(TOTAL_VALID_FMTS)
            }
        )

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
    """DBDIE `InfoExtractor` register entry create schema."""

    id:                int  # we need the ID before registering it
    name:              str
    user_id:           int
    dbdv_min_id:       int
    dbdv_max_id:       int | None
    special_mode:      bool | None
    cps_id:            int
    models_ids:        ExtractorModelsIds
    date_created:      dt.datetime
    date_modified:     dt.datetime
    date_last_trained: dt.date

    def model_post_init(self, __context) -> None:
        assert self.models_ids.any()


class ExtractorOut(ExtractorCreate):
    """DBDIE `InfoExtractor` register entry output schema."""

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_sqla(cls, extractor) -> ExtractorOut:
        return cls(
            id=extractor.id,
            name=extractor.name,
            user_id=extractor.user_id,
            dbdv_min_id=extractor.dbdv_min_id,
            dbdv_max_id=extractor.dbdv_max_id,
            special_mode=extractor.special_mode,
            cps_id=extractor.cps_id,
            models_ids=ExtractorModelsIds.from_extractor(extractor),
            date_created=extractor.date_created,
            date_modified=extractor.date_modified,
            date_last_trained=extractor.date_last_trained,
        )

    def model_post_init(self, __context) -> None:
        pass  # TODO: After registering a working Extractor, reinstate the any condition
