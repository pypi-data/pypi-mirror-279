from typing import Mapping
from haskellian import either as E, iter as I, promise as P
from kv.api import KV
import numpy as np
from scoresheet_models import Model
from moveread.core import Sheet
from .images import image_boxes

async def sheet_boxes(sheet: Sheet, *, blobs: KV[bytes], models: Mapping[str, Model]) -> list[list[np.ndarray]]:
  """Returns ply-major boxes (`result[idx][version]`)"""
  model = sheet.meta and sheet.meta.model
  results = await P.all([
    image_boxes(img, model, blobs=blobs, models=models)
    for img in sheet.images
  ])
  ok_boxes = E.filter(results)
  return I.transpose_ragged(ok_boxes)