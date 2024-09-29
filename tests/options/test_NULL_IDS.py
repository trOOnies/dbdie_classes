"""Tests for NULL_IDS options script."""

import pandas as pd
from pytest import mark

from dbdie_classes.options import MODEL_TYPE as MT
from dbdie_classes.options.NULL_IDS import mt_is_null

T = True
F = False


class TestNullIds:
    @mark.parametrize(
        "mt,data,exp",
        [
            (
                MT.CHARACTER,
                [0,1,2,3,4,5,6,7,None],
                [T,T,T,F,F,F,F,F,T   ],
            ),
            (
                MT.CHARACTER,
                [4,2,1,None,6,8,1,1,5,0,None],
                [F,T,T,T   ,F,F,T,T,F,T,T   ],
            ),
            (
                MT.OFFERING,
                [0,1,2,3,4,5,6,7,None],
                [T,T,F,F,F,F,F,F,T   ],
            ),
        ],
    )
    def test_mt_is_null(self, mt, data, exp):
        assert (
            mt_is_null(pd.Series(data), mt) == pd.Series(exp)
        ).all()
