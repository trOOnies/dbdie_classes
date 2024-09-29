"""Tests for FullModelTypes options script."""

from pytest import mark, raises

from dbdie_classes.options.FMT import assert_mt_and_pt, from_fmt, from_fmts, to_fmt
from dbdie_classes.options import MODEL_TYPE as MT
from dbdie_classes.options import PLAYER_TYPE as PT


class TestFMT:
    @mark.parametrize(
        "fmt,mt,pt,ifk",
        [
            ("perks__killer",      "perks",      "killer", True),
            ("perks__surv",        "perks",      "surv",   False),
            ("offering__killer",   "offering",   "killer", True),
            ("offering__surv",     "offering",   "surv",   False),
            ("anotherfmt__killer", "anotherfmt", "killer", True),
            ("anotherfmt__surv",   "anotherfmt", "surv",   False),
            ("points",             "points",     None,     None),
            ("prestige",           "prestige",   None,     None),
            ("anotherfmt",         "anotherfmt", None,     None),
        ],
    )
    def test_fmt(self, fmt, mt, pt, ifk):
        assert from_fmt(fmt) == (mt, pt, ifk)
        assert to_fmt(mt, ifk) == fmt

    @mark.parametrize(
        "success,mt,pt",
        [
            (True,  MT.PERKS,      PT.KILLER),
            (True,  MT.PERKS,      PT.SURV),
            (True,  MT.OFFERING,   PT.KILLER),
            (True,  MT.OFFERING,   PT.SURV),
            (False, "anotherfmt",  PT.KILLER),
            (False, "anotherfmt",  PT.SURV),
            (True,  MT.POINTS,     None),
            (True,  MT.PRESTIGE,   None),
            (False, "anotherfmt",  None),
        ],
    )
    def test_assert_mt_and_pt(self, success, mt, pt):
        if success:
            assert_mt_and_pt(mt, pt)
        else:
            with raises(AssertionError):
                assert_mt_and_pt(mt, pt)

    @mark.parametrize(
        "fmts,mts,pts,ifks",
        [
            (
                ["perks__killer", "perks__surv"],
                ["perks", "perks"],
                ["killer", "surv"],
                [True, False],
            ),
            (
                ["offering__killer", "item__surv", "points"],
                ["offering", "item", "points"],
                ["killer", "surv", None],
                [True, False, None],
            ),
        ],
    )
    def test_fmts(self, fmts, mts, pts, ifks):
        assert from_fmts(fmts) == (mts, pts, ifks)
