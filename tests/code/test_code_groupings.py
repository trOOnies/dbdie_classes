"""Tests for groupings extra code."""

from pytest import mark, raises

from dbdie_classes.options import SQL_COLS
from dbdie_classes.code.groupings import check_strict


class TestCodeGroupings:
    @mark.parametrize(
        "success,strict,sqld",
        [
            (False,  True, {}),
            (True,  False, {}),
            (True,   True, {SQL_COLS.CHARACTER[0]: 1}),
            (True,  False, {SQL_COLS.CHARACTER[0]: 1}),
            (True,   True, {SQL_COLS.STATUS[0]: 1}),
            (True,  False, {SQL_COLS.STATUS[0]: 1}),
            (False,  True, {SQL_COLS.CHARACTER[0]: 1, SQL_COLS.STATUS[0]: 2}),
            (True,  False, {SQL_COLS.CHARACTER[0]: 1, SQL_COLS.STATUS[0]: 2}),
            (False,  True, {SQL_COLS.ITEM[0]: 1, SQL_COLS.PERKS[2]: 2}),
            (True,  False, {SQL_COLS.ITEM[0]: 1, SQL_COLS.PERKS[2]: 2}),
            (False,  True, {SQL_COLS.CHARACTER[0]: 1, SQL_COLS.STATUS[0]: 2, SQL_COLS.ADDONS[1]: 3}),
            (True,  False, {SQL_COLS.CHARACTER[0]: 1, SQL_COLS.STATUS[0]: 2, SQL_COLS.ADDONS[1]: 3}),
        ],
    )
    def test_check_strict(self, success, strict, sqld):
        if success:
            check_strict(strict, sqld)
        else:
            with raises(
                AssertionError,
                match= "There can't be different model types in strict mode",
            ):
                check_strict(strict, sqld)
