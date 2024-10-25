"""Classes of predictable groupings."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from dbdie_classes.options.PLAYER_TYPE import ifk_to_pt
from dbdie_classes.options.FMT import from_fmts

if TYPE_CHECKING:
    from dbdie_classes.base import (
        FullModelType,
        IsForKiller,
        ModelType,
        PlayerType,
        PredTuple,
    )


@dataclass(kw_only=True)
class PredictableTuple:
    """Predictable tuple: full model type, model type and killer boolean."""
    fmt: "FullModelType"
    mt:  "ModelType"
    ifk: "IsForKiller"

    def to_tuple(self) -> "PredTuple":
        """Return data as a (predictable) tuple."""
        return self.fmt, self.mt, self.ifk


@dataclass(eq=False, kw_only=True)
class PredictableTuples:
    """Predictable types: full model types, model types and killer boolean.
    The 3 lists must be synched so that they can be looped at the same time.
    """
    pred_tuples: list[PredictableTuple]
    index: int = 0  # ! DO NOT USE

    @classmethod
    def from_fmts(cls, fmts: list["FullModelType"]) -> PredictableTuples:
        """Create `PredictableTuples` from a list of full model types."""
        mts, _, ifks = from_fmts(fmts)
        return cls.from_lists(fmts, mts, ifks)

    @classmethod
    def from_lists(
        cls,
        fmts: list["FullModelType"],
        mts: list["ModelType"],
        ifks: list["IsForKiller"],
    ) -> PredictableTuples:
        """Create `PredictableTuples` from 3 synched lists."""
        return cls(
            pred_tuples=[
                PredictableTuple(fmt=fmt, mt=mt, ifk=ifk)
                for fmt, mt, ifk in zip(fmts, mts, ifks)
            ]
        )

    def __iter__(self):
        return self

    def __next__(self) -> PredictableTuple:
        try:
            pred_tuple = self.pred_tuples[self.index]
        except IndexError:
            self.index = 0
            raise StopIteration
        self.index += 1
        return pred_tuple

    @property
    def fmts(self) -> list["FullModelType"]:
        """Full model types."""
        return [pred_tuple.fmt for pred_tuple in self]

    @property
    def mts(self) -> list["ModelType"]:
        """Model types."""
        return [pred_tuple.mt for pred_tuple in self]

    @property
    def ifks(self) -> list["IsForKiller"]:
        """Killer booleans."""
        return [pred_tuple.ifk for pred_tuple in self]

    @property
    def pts(self) -> list["PlayerType"]:
        """Player types."""
        return [ifk_to_pt(pred_tuple.ifk) for pred_tuple in self]

    def to_lists(self) -> tuple[list["FullModelType"], list["ModelType"], list["IsForKiller"]]:
        """Return data as a 3-tuple of lists."""
        return self.fmts, self.mts, self.ifks
