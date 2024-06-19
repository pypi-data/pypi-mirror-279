from typing import Sequence, Mapping
import asyncio
from kv.api import KV
from haskellian import Either, Left, IsLeft, Right, iter as I
import numpy as np
from scoresheet_models import Model
from moveread.core import Player
from moveread.labels import export, ChessError
from .sheets import sheet_boxes

async def player_boxes(player: Player, *, blobs: KV[bytes], models: Mapping[str, Model]) -> list[list[np.ndarray]]:
  """Returns ply-major boxes (`result[ply][img_version]`)"""
  boxes = await asyncio.gather(*[sheet_boxes(sheet, blobs=blobs, models=models) for sheet in player.sheets])
  return list(I.flatten(boxes))

def player_labels(player: Player, pgn: Sequence[str]) -> Either[ChessError, Sequence[str]]:
  return Right(pgn) if player.meta is None else export(pgn, player.meta)

async def player_samples(
  player: Player, pgn: Sequence[str], *,
  blobs: KV[bytes], models: Mapping[str, Model]
) -> Either[ChessError, list[list[tuple[np.ndarray, str]]]]:
  """Returns ply-major samples (`result[ply][img_version]`)"""
  try:
    labels = player_labels(player, pgn).unsafe()
    boxes = await player_boxes(player, blobs=blobs, models=models)
    return Right([
      [(b, lab) for b in bxs]
      for bxs, lab in zip(boxes, labels)
    ])
  except IsLeft as e:
    return Left(e.value)