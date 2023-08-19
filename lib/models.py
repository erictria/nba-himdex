'''
File with all the data structures used for this project
'''

from typing import TypedDict, List, Optional

class PlayerGameLog(TypedDict):
    player_id: str
    player_name: str
    team_id: str
    game_id: str
    fgm: int
    ftm: int
    ast: int
    dreb: int
    stl: int
    blk: int
    plus_minus: int
    min: int

class PlayerGameTotals(TypedDict):
    player_id: str
    player_name: str
    team_id: str
    game_id: str
    buckets: int
    stops: int
    plus_minus: int
    min: int

class PlayerGameMetrics(TypedDict):
    player_id: str
    player_name: str
    team_id: str
    game_id: str
    plus_minus: int
    min: int
    # buckets: int
    # stops: int
    minute_percentage: float
    bucket_contribution: float
    stop_contribution: float
    bucket_contribution_rate: float
    stop_contribution_rate: float

class TeamGameLog(TypedDict):
    team_id: str
    game_id: str
    fgm: int
    ftm: int
    ast: int
    dreb: int
    stl: int
    blk: int
    min: int

class TeamGameTotals(TypedDict):
    team_id: str
    game_id: str
    buckets: int
    stops: int
    min: int