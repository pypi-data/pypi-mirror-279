# import asyncio
# from typing import Sequence, NamedTuple
# from kv.api import KV
# from haskellian import Either, Left, Right, Iter, promise as P
# from cv2 import Mat
# from moveread.core import Game
# from moveread.errors import MissingMeta
# from .players import player_labels, player_boxes, player_samples, ChessError

# def game_labels(game: Game) -> list[Either[ChessError|MissingMeta, Sequence[str]]]:
#   pgn = game.meta and game.meta.pgn
#   if pgn is None:
#     return [Left(MissingMeta('Game has no PGN annotation'))]
#   return [player_labels(player, pgn) for player in game.players]

# async def game_boxes(game: Game, *, blobs: KV[bytes]):
#   tasks = [player_boxes(player, blobs=blobs) for player in game.players]
#   return await asyncio.gather(*tasks)

# def sampleId(gameId: str, player: int, ply: int, version: int):
#   return f'{gameId}-{player}-{ply}-{version}'

# class Sample(NamedTuple):
#   id: str
#   image: Mat
#   label: str

# @P.lift
# async def game_samples(game: Game, *, blobs: KV[bytes]) -> Sequence[Either[ChessError|MissingMeta, Sample]]:
#   pgn = game.meta and game.meta.pgn
#   if pgn is None:
#     return [Left(MissingMeta('Game has no PGN annotation'))]
#   samples = await asyncio.gather(*[player_samples(player, pgn, blobs=blobs) for player in game.players])
#   return Iter(samples).iflatmap(lambda player, e: e.match(
#     lambda err: [Left(err)],
#     lambda player_samples: [
#       Right(Sample(id=sampleId(game.id, player, ply, version), image=image, label=label))
#         for ply, ply_samples in enumerate(player_samples)
#           for version, (image, label) in enumerate(ply_samples)
#     ]
#   )).sync()