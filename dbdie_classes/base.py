"""Base DBDIE classes mainly for typing reasons."""

from typing import Literal

# Model types
ModelType = Literal[
    "character",
    "perks",
    "item",
    "addons",
    "offering",
    "status",
    "points",
    "prestige",
]
PlayerStrict = Literal["killer", "surv"]
PlayerType = PlayerStrict | None
IsForKiller = bool | None
FullModelType = str  # i.e. character__killer or points
PredTuple = tuple[FullModelType, ModelType, IsForKiller]

# API
Endpoint = str  # must start with a slash
FullEndpoint = str  # host and endpoint

# Paths
Filename = str
PathToFolder = str
RelPath = str
Path = str  # absolute path

# Crops
Width = int
Height = int
ImgSize = tuple[Width, Height]
CropCoordsRaw = tuple[int, int, int, int]
EncodedInfo = tuple[int, int, tuple, int, tuple, int, int]
CropType = Literal["surv", "killer", "surv_player", "killer_player"]  # for Cropper

# SQL
TableName = str
SQLColumn = str

# Labels
MatchId = int
PlayerId = Literal[0, 1, 2, 3, 4]
LabelId = int
LabelName = str
LabelRef = dict[LabelId, LabelName]
NetId = str
ManualCheck = bool | None
Emoji = str
Probability = float  # 0.0 to 1.0
