"""Extra code for DBD version related classes."""


def check_type(other, exp_type, allow_none: bool = False) -> None:
    if not isinstance(other, exp_type):
        if allow_none and (other is None):
            pass
        else:
            raise TypeError(f"Can only compare to another {exp_type.__name__}.")


def compare_dbdv_ranges(dbdvr_self, dbdvr_other) -> bool:
    """Compare `DBDVersionRanges` (dunder eq).

    `dbdvr_self` is not None as it is the one that calls this function.
    `dbdvr_other` can be None in some cases.
    """
    if dbdvr_other is None:
        return False

    if dbdvr_self.dbdv_min != dbdvr_other.dbdv_min:
        return False
    if not dbdvr_self.bounded:
        return not dbdvr_other.bounded

    # Every other case is handled by __eq__ in DBDVersionOut
    return dbdvr_self.dbdv_max == dbdvr_other.dbdv_max


def is_left_to(dbdvr_left, dbdvr_right) -> bool:
    """Check if `dbdvr_left` is to the left of `dbdvr_right` with no interserction."""
    return dbdvr_left.bounded and (dbdvr_left.dbdv_max <= dbdvr_right.dbdv_min)


def intersect_dbdv_max(dbdvr_self, dbdvr_other):
    """Intersect max `DBDVersionOut` of 2 `DBDVersionRanges`.
    Return a DBDVersionOut or None.

    Neither dbdvr should be None by this point.
    """
    if not dbdvr_self.bounded:
        return dbdvr_other.dbdv_max
    else:
        # Every other case is handled by __lt__ in DBDVersionOut
        return (
            dbdvr_self.dbdv_max
            if dbdvr_self.dbdv_max < dbdvr_other.dbdv_max
            else dbdvr_other.dbdv_max
        )


# TODO: May be deprecated
def filter_images_with_dbdv(
    matches: list[dict],
    dbdv_min_id: int,
    dbdv_max_id: int | None,
) -> list[dict]:
    if dbdv_max_id is None:
        return [
            m for m in matches
            if m["dbdv_id"] >= dbdv_min_id
        ]
    else:
        return [
            m for m in matches
            if (
                (m["dbdv_id"] >= dbdv_min_id)
                and (m["dbdv_id"] < dbdv_max_id)
            )
        ]
