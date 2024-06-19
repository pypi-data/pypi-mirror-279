# from typing import AsyncIterable
# from moveread.core import CoreAPI
# from haskellian import either as E, asyn_iter as AI
# from .games import game_samples, Sample

# @AI.lift
# async def core_samples(core: CoreAPI) -> AsyncIterable[Sample]:
#   async for game in core.games.values():
#     if game.tag == 'left':
#       continue
#     samples = await game_samples(game.value, blobs=core.blobs).then(E.filter)
#     for x in samples:
#       yield x