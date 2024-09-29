"""Tests for PLAYER_TYPE options script."""

from pytest import mark

from dbdie_classes.options import PLAYER_TYPE as PT


class TestPlayerType:
    @mark.parametrize(
        "pt,ifk",
        [
            (PT.KILLER, True),
            (PT.SURV,   False),
            (None,      None),
        ],
    )
    def test_ifk_to_pt(self, pt, ifk):
        assert PT.ifk_to_pt(ifk) == pt
        assert PT.pt_to_ifk(pt) == ifk
