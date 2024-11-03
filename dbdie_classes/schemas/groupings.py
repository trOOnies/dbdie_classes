"""Pydantic schemas for the grouping classes."""

from __future__ import annotations

import datetime as dt
from typing import Optional
from typing_extensions import Self

from pydantic import (
    BaseModel,
    Field,
    StrictBool,
    ValidationInfo,
    field_validator,
    model_validator,
)

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
from dbdie_classes.code.groupings import (
    check_strict, labels_model_to_checks, predictables_for_sqld
)
from dbdie_classes.code.predictables import emoji_len_func
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

    name:              LabelName        = Field(..., description="Character's full name")
    ifk:              StrictBool        = Field(..., description="Is killer")
    power_name:        LabelName | None = Field(..., description="Name of the character's power (if killer)")
    perk_names:  list[LabelName]        = Field(..., description="Name of the character's perks")
    addon_names: list[LabelName] | None = Field(..., description="Names of the character's addons (if killer)")
    dbdv:          DBDVersionOut        = Field(..., description="Character release's DBD version")
    common_name:             str        = Field(..., description="Character's common name")
    emoji:                 Emoji        = Field(..., description="Character's corresponding emoji")

    @field_validator("perk_names")
    @classmethod
    def perks_must_be_three(cls, perks: list) -> list[LabelName]:
        assert len(perks) == 3, "You must provide exactly 3 perk names."
        assert len(set(perks)) == 3, "Perk names can't repeat."
        return perks

    @field_validator("emoji")
    @classmethod
    def emoji_len(cls, emoji: Emoji | None) -> Emoji | None:
        return emoji_len_func(emoji)

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

    character:    CharacterOut        = Field(..., description="Character's output schema")
    power:             ItemOut | None = Field(..., description="Character's item (if killer)")
    perks:       list[PerkOut] | None = Field(..., description="Character's perks (can be None iif id is special null)")
    addons:     list[AddonOut] | None = Field(..., description="Character's addons (if killer)")


# * Players


class PlayerIn(BaseModel):
    """Player input schema to be used for creating labels."""

    id:                PlayerId        = Field(...,  description="Player ID (0-4 both inclusive)")
    character_id:       LabelId | None = Field(None, description="Character ID", ge=0)
    perk_ids:     list[LabelId] | None = Field(None, description="Perks IDs")
    item_id:            LabelId | None = Field(None, description="Item ID", ge=0)
    addon_ids:    list[LabelId] | None = Field(None, description="Addons IDs")
    offering_id:        LabelId | None = Field(None, description="Offering ID", ge=0)
    status_id:          LabelId | None = Field(None, description="End status ID", ge=0)
    points:                 int | None = Field(None, description="Bloodpoints earned", ge=0)
    prestige:               int | None = Field(None, description="Prestige", ge=0, le=100)

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
    character:   CharacterOut = Field(..., description="Character used")
    perks:      list[PerkOut] = Field(..., description="Perks used")
    item:             ItemOut = Field(..., description="Item used")
    addons:    list[AddonOut] = Field(..., description="Addons used")
    offering:     OfferingOut = Field(..., description="Offering used")
    status:         StatusOut = Field(..., description="End status")
    points:               int = Field(..., description="Bloodpoints earned")
    prestige:             int = Field(..., description="Prestige")
    is_consistent: StrictBool = Field(True, description="[AUTOCALC] Whether all the player info is consistent")

    def model_post_init(self, __context) -> None:
        self._check_consistency()

    @property
    def ifk(self) -> IsForKiller:
        return self.character.ifk

    def _check_consistency(self) -> None:
        """Execute all consistency checks.
        It's purposefully separated so that in the future we could have
        customized self healing methods.
        """
        assert self.is_consistent
        self.is_consistent = (
            self.ifk is not None
            and not any(
                not check_killer_consistency(self.ifk, perk) for perk in self.perks
            )
            and check_killer_consistency(self.ifk, self.offering)
            and check_item_consistency(self.ifk, self.item.type_id)
            and check_addons_consistency(self.ifk, self.addons)
            and check_status_consistency(self.status.character_id, self.ifk)
        )


# * Matches


class ManualChecksIn(BaseModel):
    """Manual predictables checks input schema."""
    addons      : ManualCheck = Field(None, description="Expected manual check for addons")
    character   : ManualCheck = Field(None, description="Expected manual check for character")
    item        : ManualCheck = Field(None, description="Expected manual check for item")
    offering    : ManualCheck = Field(None, description="Expected manual check for offering")
    perks       : ManualCheck = Field(None, description="Expected manual check for perks")
    points      : ManualCheck = Field(None, description="Expected manual check for points")
    prestige    : ManualCheck = Field(None, description="Expected manual check for prestige")
    status      : ManualCheck = Field(None, description="Expected manual check for status")
    is_init     :  StrictBool = Field(False, description="[AUTOCALC] At least 1 check is not None")
    in_progress :  StrictBool = Field(False, description="[AUTOCALC] At least 1 check is true")
    completed   :  StrictBool = Field(False, description="[AUTOCALC] All checks are true")

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
        """`ManualChecks` in list form."""
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
    predictables : dict["ModelType", ManualCheck] = Field(..., description="Manual checks in a ModelType-keyed dict")
    is_init      : StrictBool = Field(False, description="[AUTOCALC] At least 1 check is not None")
    in_progress  : StrictBool = Field(False, description="[AUTOCALC] At least 1 check is true")
    completed    : StrictBool = Field(False, description="[AUTOCALC] All checks are true")

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
        """Create `ManualChecksOut` from the SQLAlchemy `Labels` model."""
        return ManualChecksOut(
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


class MatchCreate(BaseModel):
    """DBD match creation schema."""

    filename:    Filename        = Field(..., description="Match image filename")
    match_date:   dt.date | None = Field(..., description="Date of the match")
    dbdv_id:          int | None = Field(..., description="DBD game version of the match")
    special_mode:    bool | None = Field(..., description="Whether the match is a special game mode")
    user_id:          int | None = Field(..., description="User ID of the match's uploader", ge=0)
    extr_id:          int | None = Field(..., description="ID of the InfoExtractor used for extraction", ge=0)
    kills:            int | None = Field(..., description="Total kills of the match", ge=0, le=4)


class MatchOut(MatchCreate):
    """DBD match output schema."""

    id:            MatchId     = Field(..., description="ID of the match")
    date_created:  dt.datetime = Field(..., description="Creation datetime")
    date_modified: dt.datetime = Field(..., description="Last modification datetime")


class VersionedFolderUpload(BaseModel):
    """DBD-versioned folder to upload."""

    dbdv_name:            str = Field(..., description="Game full patch identification")
    special_mode: bool | None = Field(..., description="Whether the matches are a special game mode")


class LabelsCreate(BaseModel):
    """Labels creation schema."""

    match_id:       MatchId        = Field(...,  description="ID of the match")
    player:         PlayerIn       = Field(...,  description="Player schema")
    user_id:        int | None     = Field(None, description="User ID of the match's uploader", ge=0)
    extr_id:        int | None     = Field(None, description="ID of the InfoExtractor used for extraction", ge=0)
    manual_checks:  ManualChecksIn = Field(...,  description="Manual predictables checks")


class LabelsOut(LabelsCreate):
    """Labels output schema."""

    date_modified:  dt.datetime     = Field(..., description="Last modification datetime")
    manual_checks:  ManualChecksOut = Field(..., description="Manual predictables checks")

    @classmethod
    def from_labels(cls, labels) -> LabelsOut:
        """Create `LabelsOut` from SQLAlchemy labels."""
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
    version:       DBDVersionOut
    players:       list[PlayerOut]
    kills:         int = Field(-1, ge=-1, le=4)  # ! do not use
    is_consistent: StrictBool = True  # ! do not use

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
