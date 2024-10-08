"""Extra code for DBD version related classes."""


def compare_dbdv_ranges(dbdvr_self, dbdvr_other) -> bool:
    if dbdvr_self._id != dbdvr_other._id:
        return False
    if not (dbdvr_self.bounded or dbdvr_other.bounded):
        return True
    return (
        (dbdvr_self._max_id == dbdvr_other._max_id)
        if (dbdvr_self.bounded == dbdvr_other.bounded)
        else False
    )


def get_max_id(dbdvr_self, dbdvr_other):
    if not dbdvr_self.bounded:
        return dbdvr_other.max_id
    elif not dbdvr_other.bounded:
        return dbdvr_self.max_id
    else:
        _max_id = min(dbdvr_self._max_id, dbdvr_other._max_id)
        return str(_max_id)


def filter_images_with_dbdv(
    matches: list[dict],
    dbdv_min_id: int,
    dbdv_max_id: int | None,
) -> list[dict]:
    if dbdv_max_id is None:
        return [
            m for m in matches
            if m["dbd_version"]["id"] >= dbdv_min_id
        ]
    else:
        return [
            m for m in matches
            if (
                (m["dbd_version"]["id"] >= dbdv_min_id)
                and (m["dbd_version"]["id"] < dbdv_max_id)
            )
        ]
