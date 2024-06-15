from datetime import datetime
from dataclasses import dataclass, field, InitVar
from typing import List, Dict

from ..constants import *
from .games import *
from .achievements import *

from .utils import calculate_total_stats, calculate_total_xp, calculate_required_xp, alias_convert

__all__ = [
    "MinecraftPlayer",
    "VoxylPlayer",
    "VoxylPlayerInfo",
    "VoxylPlayerOverall",
    "VoxylPlayerGames",
    "VoxylPlayerGuild",
    "VoxylPlayerAchievements",
    "StatsLeaderboardPlayer",
    "LevelLeaderboardPlayer",
    "WeightedWinsLeaderboardPlayer",
    "TechniqueLeaderboardPlayer",
    "PeriodicLeaderboardPlayer",
    "GuildMember"
]

games = {
    "bedRush": BedRush,
    "bedwalls": Bedwalls,
    "bedwarsLate": BedwarsLate,
    "bedwarsMega": BedwarsMega,
    "bedwarsNormal": BedwarsNormal,
    "bedwarsRush": BedwarsRush,
    "bowFight": BowFight,
    "bridgeFight": BridgeFight,
    "flatFight": FlatFight,
    "fourWayBridge": FourWayBridge,
    "groundFight": GroundFight,
    "ladderFight": LadderFight,
    "miniwars": Miniwars,
    "obstacles": Obstacles,
    "partyGames": PartyGames,
    "pearlFight": PearlFight,
    "rankedFoursPractice": RankedFoursPractice,
    "resourceCollect": ResourceCollect,
    "resourceOldCollect": ResourceOldCollect,
    "stickFight": StickFight,
    "sumo": Sumo,
    "sumoDuels": SumoDuels,
    "voidFight": VoidFight
}

@dataclass
class MinecraftPlayer:
    _data: InitVar[Dict] = None
    name: str = None
    uuid: str = None
    formattedUUID: str = None

    def __post_init__(self, _data: dict):
        self.name = _data.get("username", None)
        self.formattedUUID = _data.get("uuid", None)
        self.uuid = self.formattedUUID.replace("-", "") if self.formattedUUID else None

@dataclass
class VoxylPlayer:
    _gen_data: InitVar[Dict] = None
    _over_data: InitVar[Dict] = None
    _game_data: InitVar[Dict] = None
    _guild_data: InitVar[Dict] = None
    _ach_data: InitVar[List] = None
    uuid: str = None
    name: str = None
    last_login_time: datetime = None
    last_login_time_raw: int = 0
    rank: str = None
    level: int = 0
    xp: int = 0
    required_xp: int = 0
    weightedwins: int = 0
    wins: int = 0
    finals: int = 0
    kills: int = 0
    beds: int = 0
    guild_id: int = None

    bedRush: BedRush = field(init=False)
    bedwalls: Bedwalls = field(init=False)
    bedwarsLate: BedwarsLate = field(init=False)
    bedwarsMega: BedwarsMega = field(init=False)
    bedwarsNormal: BedwarsNormal = field(init=False)
    bedwarsRush: BedwarsRush = field(init=False)
    bowFight: BowFight = field(init=False)
    bridgeFight: BridgeFight = field(init=False)
    flatFight: FlatFight = field(init=False)
    fourWayBridge: FourWayBridge = field(init=False)
    groundFight: GroundFight = field(init=False)
    ladderFight: LadderFight = field(init=False)
    miniwars: Miniwars = field(init=False)
    obstacles: Obstacles = field(init=False)
    partyGames: PartyGames = field(init=False)
    pearlFight: PearlFight = field(init=False)
    rankedFoursPractice: RankedFoursPractice = field(init=False)
    resourceCollect: ResourceCollect = field(init=False)
    resourceOldCollect: ResourceOldCollect = field(init=False)
    stickFight: StickFight = field(init=False)
    sumo: Sumo = field(init=False)
    sumoDuels: SumoDuels = field(init=False)
    voidFight: VoidFight = field(init=False)

    achievements: List[Achievement] = field(default_factory=list)

    def __post_init__(self, _gen_data: dict, _over_data: dict, _game_data: dict, _guild_data: dict, _ach_data: List):
        data = alias_convert({**_gen_data, **_over_data, **_guild_data}, "PLAYER")
        for i in data:
            setattr(self, i, data[i])

        total = calculate_total_stats(_game_data)
        self.wins = total.get("wins", 0)
        self.finals = total.get("finals", 0)
        self.kills = total.get("kills", 0)
        self.beds = total.get("beds", 0)

        self.required_xp = calculate_required_xp(self.level)
        self.total_xp = calculate_total_xp(self.level, self.xp)

        self.last_login_time = datetime.fromtimestamp(self.last_login_time_raw).strftime("%I:%M %p on %B %d, %Y")

        for game, model in games.items():
            data = alias_convert(_game_data, game, model)
            setattr(self, game, model(**data))

        self.achievements = _ach_data

@dataclass
class VoxylPlayerInfo:
    _data: InitVar[Dict] = None
    uuid: str = None
    name: str = None
    last_login_time: datetime = None
    last_login_time_raw: int = 0
    rank: str = None

    def __post_init__(self, _data: dict):
        data = alias_convert(_data, "PLAYER")
        for i in data:
            setattr(self, i, data[i])

        self.last_login_time = datetime.fromtimestamp(self.last_login_time_raw).strftime("%I:%M %p on %B %d, %Y")

@dataclass
class VoxylPlayerOverall:
    _data: InitVar[Dict] = None
    uuid: str = None
    name: str = None
    level: int = 0
    xp: int = 0

    def __post_init__(self, _data: dict):
        data = alias_convert(_data, "PLAYER")
        for i in data:
            setattr(self, i, data[i])

@dataclass
class VoxylPlayerGames:
    _data: InitVar[Dict] = None
    uuid: str = None
    name: str = None
    bedRush: BedRush = field(init=False)
    bedwalls: Bedwalls = field(init=False)
    bedwarsLate: BedwarsLate = field(init=False)
    bedwarsMega: BedwarsMega = field(init=False)
    bedwarsNormal: BedwarsNormal = field(init=False)
    bedwarsRush: BedwarsRush = field(init=False)
    bowFight: BowFight = field(init=False)
    bridgeFight: BridgeFight = field(init=False)
    flatFight: FlatFight = field(init=False)
    fourWayBridge: FourWayBridge = field(init=False)
    groundFight: GroundFight = field(init=False)
    ladderFight: LadderFight = field(init=False)
    miniwars: Miniwars = field(init=False)
    obstacles: Obstacles = field(init=False)
    partyGames: PartyGames = field(init=False)
    pearlFight: PearlFight = field(init=False)
    rankedFoursPractice: RankedFoursPractice = field(init=False)
    resourceCollect: ResourceCollect = field(init=False)
    resourceOldCollect: ResourceOldCollect = field(init=False)
    stickFight: StickFight = field(init=False)
    sumo: Sumo = field(init=False)
    sumoDuels: SumoDuels = field(init=False)
    voidFight: VoidFight = field(init=False)

    def __post_init__(self, _data: dict):
        for game, model in games.items():
            data = alias_convert(_data, game, model)
            setattr(self, game, model(**data))

@dataclass
class VoxylPlayerGuild:
    _data: InitVar[Dict] = None
    uuid: str = None
    name: str = None
    guild_id: int = 0
    role: str = None
    join_date: datetime = None
    join_date_raw: int = 0

    def __post_init__(self, _data: dict):
        data = alias_convert(_data, "PLAYER")
        for i in data:
            setattr(self, i, data[i])

        self.join_date = datetime.fromtimestamp(self.join_date_raw).strftime("%I:%M %p on %B %d, %Y")

@dataclass
class VoxylPlayerAchievements:
    _data: InitVar[Dict] = None
    uuid: str = None
    name: str = None
    achievements: List[Achievement] = field(default_factory=list)

    def __post_init__(self, _data: dict):
        self.achievements = _data

@dataclass
class StatsLeaderboardPlayer:
    _data: InitVar[Dict] = None
    uuid: str = None
    level: int = 0
    weightedwins: int = 0
    position: int = 0

    def __post_init__(self, _data: dict):
        data = alias_convert(_data, "LEADERBOARD")
        for i in data:
            setattr(self, i, data[i])

@dataclass
class LevelLeaderboardPlayer(StatsLeaderboardPlayer):
    leaderboard: str = "level"

@dataclass
class WeightedWinsLeaderboardPlayer(StatsLeaderboardPlayer):
    leaderboard: str = "weightedwins"

@dataclass
class TechniqueLeaderboardPlayer:
    _data: InitVar[Dict] = None
    uuid: str = None
    technique_time: float = 0
    date_submitted: datetime = 0
    date_submitted_raw: int = 0
    position: int = 0

    def __post_init__(self, _data: dict):
        data = alias_convert(_data, "LEADERBOARD")
        for i in data:
            setattr(self, i, data[i])

        self.technique_time = int(self.technique_time)
        self.date_submitted = datetime.fromtimestamp(self.date_submitted_raw).strftime("%I:%M %p on %B %d, %Y")

@dataclass
class PeriodicLeaderboardPlayer:
    _data: InitVar[Dict] = None
    uuid: str = None
    wins: int = 0
    position: int = 0

    def __post_init__(self, _data: dict):
        data = alias_convert(_data, "LEADERBOARD")
        for i in data:
            setattr(self, i, data[i])

@dataclass
class GuildMember:
    _data: InitVar[Dict] = None
    uuid: str = None
    role: str = None
    join_date: datetime = 0
    join_date_raw: int = 0

    def __post_init__(self, _data: dict):
        data = alias_convert(_data, "GUILD_MEMBER")
        for i in data:
            setattr(self, i, data[i])

        self.join_date = datetime.fromtimestamp(self.join_date_raw).strftime("%I:%M %p on %B %d, %Y")