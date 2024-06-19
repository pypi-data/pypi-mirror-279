from typing import Mapping
from haskellian import Either, Left, Right, promise as P
from scoresheet_models import Model
import pure_cv as vc
import numpy as np
from kv.api import KV
from moveread.core import Image
from moveread.boxes import export, exportable
from moveread.errors import MissingMeta

@P.lift
async def image_boxes(
  image: Image, model: str | None = None, *, blobs: KV[bytes],
  models: Mapping[str, Model]
) -> Either[MissingMeta, list[np.ndarray]]:
  if image.meta is None:
    return Left(MissingMeta('Empty image meta'))
  match exportable(image.meta, model):
    case Left(err):
      return Left(err) # type: ignore
    case Right(ann):
      img = (await blobs.read(image.url)).unsafe()
      mat = vc.decode(img)
      return Right(export(mat, ann, models=models))