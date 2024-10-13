"""Tests for DBDVersion."""

from pytest import mark

from dbdie_classes.schemas.helpers import DBDVersionOut


class TestDBDVersion:
    def test_dbdversion_dunder_str(self):
        dbdv = DBDVersionOut("8", "1", "1")
        assert str(dbdv) == "8.1.1"
        dbdv = DBDVersionOut("8", "1", "1a")
        assert str(dbdv) == "8.1.1a"

    def test_dbdversion_from_str(self):
        dbvd1 = DBDVersionOut.from_str("8.5.0")
        assert dbvd1.major == "8"
        assert dbvd1.minor == "5"
        assert dbvd1.patch == "0"
        assert dbvd1.is_not_ptb

        dbvd2 = DBDVersionOut.from_str("8.5.0a")
        assert dbvd2.major == "8"
        assert dbvd2.minor == "5"
        assert dbvd2.patch == "0a"
        assert dbvd2.is_not_ptb

        dbvd3 = DBDVersionOut.from_str("7.2.0-ptb")
        assert dbvd3.major == "7"
        assert dbvd3.minor == "2"
        assert dbvd3.patch == "0"
        assert not dbvd3.is_not_ptb

    @mark.parametrize(
        "ineq,v1,v2",
        [
            ( 0, "7.5.0",     "7.5.0"    ),
            ( 0, "1.5.0",     "1.5.0"    ),
            ( 1, "1.5.0",     "7.5.0"    ),
            ( 1, "7.5.0",     "7.6.0"    ),
            ( 1, "7.5.0",     "7.9.0"    ),
            (-1, "7.9.0",     "7.5.0"    ),
            ( 1, "7.5.0",     "7.5.0a"   ),
            (-1, "7.5.0a",    "7.5.0"    ),
            ( 1, "7.5.0-ptb", "7.5.0"    ),
            (-1, "7.5.0",     "7.5.0-ptb"),
            (-1, "8.0.0-ptb", "7.5.0"    ),
            ( 1, "7.5.0-ptb", "8.0.0"    ),
            ( 0, "7.5.0-ptb", "7.5.0-ptb"),
            ( 1, "7.5.0-ptb", "8.0.0-ptb"),
        ],
    )
    def test_dbdversion_dunder_ineq(self, ineq, v1, v2):
        dbdv1 = DBDVersionOut.from_str(v1)
        dbdv2 = DBDVersionOut.from_str(v2)
        if ineq == -1:
            assert dbdv1 > dbdv2
        elif ineq == 0:
            assert dbdv1 == dbdv2
        elif ineq == 1:
            assert dbdv1 < dbdv2
        else:
            raise ValueError
