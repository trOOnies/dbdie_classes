"""Tests for DBDVersionRange."""

from pytest import mark, raises

from dbdie_classes.schemas.helpers import DBDVersionOut, DBDVersionRange


class TestDBDVersionRange:
    # * DBD Version

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

    # * DBD Version Range

    def test_dbdvr_dunder_post_init(self):
        for dbd_vr in [
            DBDVersionRange("7.5.0"),
            DBDVersionRange.from_dbd_versions(
                DBDVersionOut("7", "5", "0"),
                None,
            ),
        ]:
            assert not dbd_vr.bounded
            assert dbd_vr._id.major == "7"
            assert str(dbd_vr._id) == "7.5.0"
            assert dbd_vr._max_id is None
            assert dbd_vr._id.is_not_ptb

        for dbd_vr_2 in [
            DBDVersionRange("7.5.0", "8.0.0"),
            DBDVersionRange.from_dbd_versions(
                DBDVersionOut("7", "5", "0"),
                DBDVersionOut("8", "0", "0"),
            ),
        ]:
            assert dbd_vr_2.bounded
            assert dbd_vr_2._id.major == "7"
            assert dbd_vr_2._max_id.major == "8"
            assert str(dbd_vr_2._id) == "7.5.0"
            assert str(dbd_vr_2._max_id) == "8.0.0"
            assert dbd_vr_2._id.is_not_ptb
            assert dbd_vr_2._max_id.is_not_ptb

        for dbd_vr_3 in [
            DBDVersionRange("8.0.0-ptb", "8.0.0"),
            DBDVersionRange.from_dbd_versions(
                DBDVersionOut("8", "0", "0", is_not_ptb=False),
                DBDVersionOut("8", "0", "0"),
            ),
        ]:
            assert dbd_vr_3.bounded
            assert dbd_vr_3._id.major == "8"
            assert dbd_vr_3._max_id.major == "8"
            assert str(dbd_vr_3._id) == "8.0.0-ptb"
            assert str(dbd_vr_3._max_id) == "8.0.0"
            assert not dbd_vr_3._id.is_not_ptb
            assert dbd_vr_3._max_id.is_not_ptb

    def test_dbdvr_dunder_post_init_raises(self):
        with raises(AssertionError):
            DBDVersionRange("8.0.0", "8.0.0")
        with raises(AssertionError):
            DBDVersionRange.from_dbd_versions(
                DBDVersionOut("8", "0", "0"),
                DBDVersionOut("8", "0", "0"),
            )

        with raises(AssertionError):
            DBDVersionRange("8.0.0", "7.5.0")
        with raises(AssertionError):
            DBDVersionRange.from_dbd_versions(
                DBDVersionOut("8", "0", "0"),
                DBDVersionOut("7", "5", "0"),
            )

        with raises(AssertionError):
            DBDVersionRange("8.0.0", "8.0.0-ptb")
        with raises(AssertionError):
            DBDVersionRange.from_dbd_versions(
                DBDVersionOut("8", "0", "0"),
                DBDVersionOut("8", "0", "0", is_not_ptb=False),
            )

    def test_dbdvr_dunder_str(self):
        dbd_vr = DBDVersionRange("7.5.0")
        assert str(dbd_vr) == ">=7.5.0"

        dbd_vr = DBDVersionRange("7.5.0", "8.0.0")
        assert str(dbd_vr) == ">=7.5.0,<8.0.0"

    @mark.parametrize(
        "eq,v1,v1_max,v2,v2_max",
        [
            ( True, "7.5.0", "8.0.0", "7.5.0",  "8.0.0"),
            ( True, "1.5.0", "4.5.0", "1.5.0",  "4.5.0"),
            (False, "7.5.0", "8.0.0", "7.6.0",  "8.0.0"),
            (False, "7.5.0", "8.0.0", "7.5.0",  "9.0.0"),
            (False, "7.5.0", "8.0.0", "7.9.0",  "8.1.2"),
            (False, "7.5.0", "8.0.0", "7.5.0a", "8.0.0"),
        ],
    )
    def test_dbdvr_dunder_eq(self, eq, v1, v1_max, v2, v2_max):
        dbd_vr_1 = DBDVersionRange(v1, v1_max)
        dbd_vr_2 = DBDVersionRange(v2, v2_max)
        assert (dbd_vr_1 == dbd_vr_2) == eq

    @mark.parametrize(
        "cont,cont_unbounded,v_min,v_max,v",
        [
            (False, False, "7.5.0", "8.0.0", "7.0.0" ),
            (False, False, "7.5.0", "8.0.0", "7.4.9a"),
            ( True,  True, "7.5.0", "8.0.0", "7.5.0" ),
            ( True,  True, "7.5.0", "8.0.0", "7.5.0a"),
            ( True,  True, "7.5.0", "8.0.0", "7.9.0" ),
            ( True,  True, "7.5.0", "8.0.0", "7.9.0a"),
            ( True,  True, "7.5.0", "8.0.0", "7.9.9" ),
            ( True,  True, "7.5.0", "8.0.0", "7.9.9a"),
            (False,  True, "7.5.0", "8.0.0", "8.0.0" ),
            (False,  True, "7.5.0", "8.0.0", "8.0.0a"),
            (False,  True, "7.5.0", "8.0.0", "8.0.1" ),
            (False,  True, "7.5.0", "8.0.0", "9.0.0" ),
            (False, False, "1.5.0", "4.5.0", "1.0.0" ),
            ( True,  True, "1.5.0", "4.5.0", "3.0.0" ),
            (False,  True, "1.5.0", "4.5.0", "7.5.0" ),
        ],
    )
    def test_dbdvr_dunder_contains(self, cont, cont_unbounded, v_min, v_max, v):
        dbdvr = DBDVersionRange(v_min, v_max)
        dbdv = DBDVersionOut(*v.split("."))
        assert (dbdv in dbdvr) == cont

        dbdvr = DBDVersionRange(v_min)
        dbdv = DBDVersionOut(*v.split("."))
        assert (dbdv in dbdvr) == cont_unbounded

    @mark.parametrize(
        "int_min,int_max,vr1_min,vr1_max,vr2_min,vr2_max",
        [
            ("8.0.0",     "8.5.0", "8.0.0",     "8.5.0", "8.0.0",     "8.5.0"),
            ("8.0.0",     "8.5.0", "8.0.0",     "9.0.0", "8.0.0",     "8.5.0"),
            ("8.0.0",     "8.5.0", "7.5.0",     "8.5.0", "8.0.0",     "8.5.0"),
            ("8.0.0",     "8.5.0", "7.5.0",     "9.0.0", "8.0.0",     "8.5.0"),
            ("8.0.0-ptb", "8.0.0", "7.5.0",     "9.0.0", "8.0.0-ptb", "8.0.0"),
            ("8.0.0-ptb", "8.0.0", "8.0.0-ptb", "8.1.0", "8.0.0-ptb", "8.0.0"),
            ("8.0.0",     "8.5.0", "8.0.0",     "8.5.0", "8.0.0",        None),
            ("8.0.0",     "8.5.0", "8.0.0",     "8.5.0", "7.0.0",        None),
            ("8.0.0",     "8.5.0", "7.0.0",     "8.5.0", "8.0.0",        None),
            ("8.5.0",        None, "8.0.0",        None, "8.5.0",        None),
            ("8.0.0",        None, "8.0.0",        None, "8.0.0",        None),
            ("8.0.0",        None, "8.0.0-ptb",    None, "8.0.0",        None),
        ],
    )
    def test_dbdvr_dunder_and(
        self,
        int_min,
        int_max,
        vr1_min,
        vr1_max,
        vr2_min,
        vr2_max,
    ):
        vr1 = DBDVersionRange(vr1_min, vr1_max)
        vr2 = DBDVersionRange(vr2_min, vr2_max)
        vr_int = DBDVersionRange(int_min, int_max)
        assert vr_int == vr1 & vr2
        assert vr_int == vr2 & vr1

    # def test_setup_folder  # TODO
