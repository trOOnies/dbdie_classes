"""Types of crops made by the Croppers."""

SURV          = "surv"
KILLER        = "killer"
SURV_PLAYER   = "surv_player"
KILLER_PLAYER = "killer_player"

ALL = [SURV, KILLER, SURV_PLAYER, KILLER_PLAYER]
DEFAULT_CROP_TYPES_SEQ = [[SURV, KILLER], [SURV_PLAYER, KILLER_PLAYER]]