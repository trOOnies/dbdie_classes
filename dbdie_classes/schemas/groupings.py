"""Pydantic schemas for the grouping classes."""

from __future__ import annotations

import datetime as dt
from typing import Optional
from typing_extensions import Self

from pydantic import BaseModel, Field, ValidationInfo, field_validator, model_validator

from dbdie_classes.base import (
    Emoji,
    Filename,
    IsForKiller,
    LabelId,
    LabelName,
    ManualCheck,
    MatchId,
    ModelType,
    PlayerId,
)
from dbdie_classes.version import DBDVersion
from dbdie_classes.code.groupings import (
    check_strict, labels_model_to_checks, predictables_for_sqld
)
from dbdie_classes.code.schemas import (
    check_addons_consistency,
    check_item_consistency,
    check_killer_consistency,
    check_status_consistency,
)
from dbdie_classes.schemas.helpers import DBDVersionOut
from dbdie_classes.schemas.predictables import (
    AddonOut,
    CharacterOut,
    ItemOut,
    OfferingOut,
    PerkOut,
    StatusOut,
)
from dbdie_classes.options.MODEL_TYPE import ALL as ALL_MT


# * Full characters


class FullCharacterCreate(BaseModel):
    """Full character creation schema.
    Includes the creation perks and addons (if addons apply).
    DBD game version must already exist in the database.

    Note: This schema shouldn't be used for creating legendary outfits that
    use base_char_id. Please use CharacterCreate instead.
    """

    name:              LabelName
    ifk:                    bool
    power_name:        LabelName | None
    perk_names:  list[LabelName]
    addon_names: list[LabelName] | None
    dbd_version:      DBDVersion
    common_name:             str
    emoji:                 Emoji

    @field_validator("perk_names")
    @classmethod
    def perks_must_be_three(cls, perks: list) -> list[LabelName]:
        assert len(perks) == 3, "You must provide exactly 3 perk names."
        assert len(set(perks)) == 3, "Perk names can't repeat."
        return perks

    @field_validator("emoji")
    @classmethod
    def emoji_len(cls, emoji: str) -> Emoji:
        assert len(emoji) == 1, "The emoji attribute can only be 1 character."
        return emoji

    @model_validator(mode="after")
    def check_power_name(self) -> Self:
        assert (
            (self.power_name is not None) == self.ifk
        ), "Killers must have a power name, survivors can't."
        return self

    @model_validator(mode="after")
    def check_total_addons(self) -> Self:
        if self.ifk:
            assert (
                (self.addon_names is not None) and (len(self.addon_names) == 20)
            ), "You must provide exactly 20 killer addon names."
        else:
            if self.addon_names is not None:
                assert not self.addon_names, "Survivors can't have addon names."
                self.addon_names = None
        return self


class FullCharacterOut(BaseModel):
    """Full character output schema."""

    character:    CharacterOut
    power:             ItemOut | None
    perks:       list[PerkOut]
    addons:     list[AddonOut] | None
    common_name:        str | None
    # proba:    Probability | None = None
    ifk:        IsForKiller
    base_char_id:   LabelId | None
    dbdv_id:            int | None
    emoji:            Emoji | None


# * Players


class PlayerIn(BaseModel):
    """Player input schema to be used for creating labels."""

    id:                PlayerId
    character_id:       LabelId | None = Field(None, ge=0)
    perk_ids:     list[LabelId] | None = None
    item_id:            LabelId | None = Field(None, ge=0)
    addon_ids:    list[LabelId] | None = None
    offering_id:        LabelId | None = Field(None, ge=0)
    status_id:          LabelId | None = Field(None, ge=0)
    points:                 int | None = Field(None, ge=0)
    prestige:               int | None = Field(None, ge=0, le=100)

    @classmethod
    def from_labels(cls, labels) -> PlayerIn:
        try:
            perks = [labels.perks_0, labels.perks_1, labels.perks_2, labels.perks_3]
            perks = perks if all(p is not None for p in perks) else None
        except AttributeError:
            perks = None

        try:
            addons = [labels.addons_0, labels.addons_1]
            addons = addons if all(a is not None for a in addons) else None
        except AttributeError:
            addons = None

        return PlayerIn(
            id=labels.player_id,
            character_id=getattr(labels, "character", None),
            perk_ids=perks,
            item_id=getattr(labels, "item", None),
            addon_ids=addons,
            offering_id=getattr(labels, "offering", None),
            status_id=getattr(labels, "status", None),
            points=getattr(labels, "points", None),
            prestige=getattr(labels, "prestige", None),
        )

    @field_validator("perk_ids", "addon_ids")
    @classmethod
    def count_ids(
        cls,
        v: Optional[list[int]],
        info: ValidationInfo,
    ) -> Optional[list[LabelId]]:
        if v is None:
            return v
        elif info.field_name == "perk_ids":
            assert len(v) == 4, "There can only be 4 perks or None"
            assert all(p >= 0 for p in v), "Perk ids can't be negative"
        elif info.field_name == "addon_ids":
            assert len(v) == 2, "There can only be 2 addons or None"
            assert all(p >= 0 for p in v), "Addon ids can't be negative"
        else:
            raise NotImplementedError
        return v

    def filled_predictables(self) -> list[str]:
        """Return predictables' names that are filled (fps)."""
        d = dict(self)
        del d["id"]
        return [k for k, v in d.items() if v is not None]

    def to_sqla(self, fps: list[str], strict: bool) -> dict:
        """To dict for the 'Labels' SQLAlchemy model."""
        sqld = {"player_id": self.id}
        sqld = sqld | predictables_for_sqld(self, fps)
        check_strict(strict, sqld)
        return sqld

    @staticmethod
    def flatten_predictables(info: dict) -> dict:
        new_info = {
            f"{k}_mckd": v
            for k, v in info["manual_checks"]["predictables"].items()
        }
        del info["manual_checks"]
        return info | new_info


class PlayerOut(BaseModel):
    """Player output schema as seen in created labels."""

    id:              PlayerId
    character:   CharacterOut
    perks:      list[PerkOut]
    item:             ItemOut
    addons:    list[AddonOut]
    offering:     OfferingOut
    status:         StatusOut
    points:               int
    prestige:             int
    is_consistent: Optional[bool] = None

    def model_post_init(self, __context) -> None:
        self.check_consistency()

    @property
    def ifk(self) -> IsForKiller:
        return self.character.ifk

    def check_consistency(self) -> None:
        """Execute all consistency checks.
        It's purposefully separated so that in the future we could have
        customized self healing methods.
        """
        if self.ifk is None:
            self.is_consistent = False
        elif any(
            not check_killer_consistency(self.ifk, perk) for perk in self.perks
        ):
            self.is_consistent = False
        elif not check_killer_consistency(self.ifk, self.offering):
            self.is_consistent = False
        elif not check_item_consistency(self.ifk, self.item.type_id):
            self.is_consistent = False
        elif not check_addons_consistency(self.ifk, self.addons):
            self.is_consistent = False
        elif not check_status_consistency(self.status.character_id, self.ifk):
            self.is_consistent = False
        else:
            self.is_consistent = True


# * Matches


class ManualChecksIn(BaseModel):
    """Manual predictables checks input schema."""
    addons    : ManualCheck = None
    character : ManualCheck = None
    item      : ManualCheck = None
    offering  : ManualCheck = None
    perks     : ManualCheck = None
    points    : ManualCheck = None
    prestige  : ManualCheck = None
    status    : ManualCheck = None
    is_init     : bool = False  # ! do not use
    in_progress : bool = False  # ! do not use
    completed   : bool = False  # ! do not use

    def model_post_init(self, __context) -> None:
        assert not self.is_init
        assert not self.in_progress
        assert not self.completed

        self.is_init = any(c is not None for c in self.checks)

        if not self.is_init:
            self.in_progress = False
            self.completed = False
        else:
            conds = [(c is not None and c) for c in self.checks]
            self.in_progress = any(conds)
            self.completed = all(conds)

    @property
    def checks(self) -> list[ManualCheck]:
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

    def get_filters_conds(self, labels_model) -> list[tuple]:
        """Get filters conditions for SQLAlchemy."""
        return [
            (col, chk)
            for col, chk in zip(
                labels_model_to_checks(labels_model),
                self.checks,
            )
            if chk is not None
        ]


class ManualChecksOut(BaseModel):
    """Manual predictables checks output schema."""
    predictables : dict["ModelType", ManualCheck]
    is_init      : bool = False  # ! do not use
    in_progress  : bool = False  # ! do not use
    completed    : bool = False  # ! do not use

    @property
    def checks(self) -> list[ManualCheck]:
        return [self.predictables[mt] for mt in ALL_MT]

    def model_post_init(self, __context) -> None:
        assert not self.is_init
        assert not self.in_progress
        assert not self.completed

        # Dict must have exactly all expected keys
        assert set(mt for mt in ALL_MT) == set(self.predictables.keys())

        self.is_init = any(c is not None for c in self.checks)
        conds = [(c is not None and c) for c in self.checks]
        self.in_progress = any(conds)
        self.completed = all(conds)

    @classmethod
    def from_labels(cls, labels) -> ManualChecksOut:
        mc_out = ManualChecksOut(
            predictables={
                "addons": labels.addons_mckd,
                "character": labels.character_mckd,
                "item": labels.item_mckd,
                "offering": labels.offering_mckd,
                "perks": labels.perks_mckd,
                "prestige": labels.prestige_mckd,
                "points": labels.points_mckd,
                "status": labels.status_mckd,
            }
        )
        return mc_out


class MatchCreate(BaseModel):
    """DBD match creation schema."""

    filename:       Filename
    match_date:      dt.date | None = None
    dbd_version:  DBDVersion | None = None
    special_mode:       bool | None = None
    user_id:             int | None = Field(None, ge=0)
    extr_id:             int | None = Field(None, ge=0)
    kills:               int | None = Field(None, ge=0, le=4)


class MatchOut(BaseModel):
    """DBD match output schema."""

    id:            MatchId
    filename:      Filename
    match_date:    dt.date | None
    dbd_version:   DBDVersionOut | None
    special_mode:  bool | None
    kills:         int | None
    date_created:  dt.datetime
    date_modified: dt.datetime
    user_id:       int | None
    extr_id:       int | None


class VersionedFolderUpload(BaseModel):
    """DBD-versioned folder to upload."""

    dbd_version:  DBDVersion
    special_mode: Optional[bool] = None


class VersionedMatchOut(BaseModel):
    """DBD match simplified output schema for DBD-versioned folder upload."""

    id:           MatchId
    filename:     Filename
    match_date:   dt.date | None
    dbd_version:  DBDVersionOut
    special_mode: bool | None


class LabelsCreate(BaseModel):
    """Labels creation schema."""

    match_id:       MatchId
    player:         PlayerIn
    user_id:        int | None = None
    extr_id:        int | None = None
    manual_checks:  ManualChecksIn


class LabelsOut(BaseModel):
    """Labels output schema."""

    match_id:       MatchId
    player:         PlayerIn
    date_modified:  dt.datetime
    user_id:        int | None
    extr_id:        int | None
    manual_checks:  ManualChecksOut

    @classmethod
    def from_labels(cls, labels) -> LabelsOut:
        labels_out = LabelsOut(
            match_id=labels.match_id,
            player=PlayerIn.from_labels(labels),
            date_modified=labels.date_modified,
            user_id=labels.user_id,
            extr_id=labels.extr_id,
            manual_checks=ManualChecksOut.from_labels(labels),
        )
        return labels_out


class FullMatchOut(BaseModel):
    """Labeled DBD match output schema."""

    # TODO
    version:       DBDVersion
    players:       list[PlayerOut]
    kills:         int = Field(-1, ge=-1, le=4)  # ! do not use
    is_consistent: bool = True  # ! do not use

    def model_post_init(self, __context) -> None:
        assert self.kills == -1
        assert self.is_consistent
        self.check_consistency()
        self.kills = sum(
            pl.status.is_dead if pl.status.is_dead is not None else 0
            for pl in self.players[:4]
        )

    def check_consistency(self) -> None:
        """Execute all consistency checks."""
        self.is_consistent = all(not pl.character.ifk for pl in self.players[:4])
        self.is_consistent = (
            self.is_consistent
            and (self.players[4].character.ifk is not None)
            and self.players[4].character.ifk
        )
        self.is_consistent = self.is_consistent and all(
            pl.is_consistent for pl in self.players
        )
