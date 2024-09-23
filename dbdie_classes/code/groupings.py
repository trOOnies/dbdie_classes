"""Extra code for groupings classes."""

from dbdie_classes.options import MODEL_TYPE as MT
from dbdie_classes.options import SQL_COLS


def labels_model_to_checks(labels_model):
    """Labels SQLAlchemy model to its manual check columns."""
    return [
        labels_model.addons_mckd,
        labels_model.character_mckd,
        labels_model.item_mckd,
        labels_model.offering_mckd,
        labels_model.perks_mckd,
        labels_model.points_mckd,
        labels_model.prestige_mckd,
        labels_model.status_mckd,
    ]


def predictables_for_sqld(player, fps: list[str]) -> dict:
    """Predictables to add to SQL dict."""
    sqld = {
        mt: getattr(player, MT.TO_ID_NAMES[mt])
        for mt in MT.UNIQUE_PER_PLAYER
        if MT.TO_ID_NAMES[mt] in fps
    }
    sqld = sqld | {f"{mt}_mckd": True for mt in sqld}

    if MT.TO_ID_NAMES[MT.PERKS] in fps:
        cond = player.perk_ids is not None
        sqld = sqld | {
            col: pid if cond else None
            for pid, col in zip(player.perk_ids, SQL_COLS.PERKS)
        } | {"perks_mckd": True}

    if MT.TO_ID_NAMES[MT.ADDONS] in fps:
        cond = player.addon_ids is not None
        sqld = sqld | {
            col: aid if cond else None
            for aid, col in enumerate(player.addon_ids, SQL_COLS.ADDONS)
        } | {"addons_mckd": True}

    return sqld


def check_strict(strict: bool, sqld: dict) -> None:
    if strict:
        all_fps_cols = [
            cols for cols in SQL_COLS.ALL
            if any(c in sqld for c in cols)
        ]
        assert len(all_fps_cols) == 1, "There can't be different model types in strict mode"
