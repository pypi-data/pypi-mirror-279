from typing import Sequence
from pydantic import BaseModel, ConfigDict

class Tournament(BaseModel):
  model_config = ConfigDict(extra='forbid')
  tournId: str | None = None
  # name: str | None = None
  group: str | None = None
  round: str | None = None
  board: str | None = None


class GameMeta(BaseModel):
  model_config = ConfigDict(extra='forbid')
  tournament: Tournament | None = None
  pgn: Sequence[str] | None = None
  early: bool | None = None
  """Whether the `PGN` stops before the game actually finished"""
