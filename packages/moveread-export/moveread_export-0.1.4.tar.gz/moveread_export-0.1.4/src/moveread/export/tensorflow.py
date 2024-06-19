from typing import Iterable, AsyncIterable
from jaxtyping import Float
from haskellian import iter as I
import tensorflow as tf
from cv2 import Mat
import tf.tools as tft
import tf.ocr as ocr
from moveread.core import CoreAPI
from .games import Sample
from .core import core_samples

def imgs_dataset(imgs: list[Mat]) -> tf.data.Dataset[Float[tf.Tensor, "256 53 1"]]: # type: ignore
  return tf.data.Dataset.from_tensor_slices([
    ocr.preprocess(img) for img in imgs
  ])

def export_dataset(samples: Iterable[Sample]) -> tf.data.Dataset[ocr.Example]: # type: ignore
  ids, imgs, labs = I.unzip(samples)
  Dids = tf.data.Dataset.from_tensor_slices(ids)
  Dimgs = imgs_dataset(imgs)
  Dlab = tf.data.Dataset[tft.Bytes[tf.Tensor, ""]].from_tensor_slices(labs) # type: ignore
  return tf.data.Dataset.zip(Dids, Dimgs, Dlab).map(
    lambda id, img, lab: ocr.Example(boxid=id, image=img, label=lab)
  )

async def datasets(core: CoreAPI, batch_size: int = 1024) -> AsyncIterable[tf.data.Dataset]:
  async for samples in core_samples(core).batch(batch_size):
    yield export_dataset(samples)

async def export_tfrecords(core: CoreAPI, path: str, batch_size: int = 1024):
  """Export a core into TFRecords, by creating datasets of `batch_size` and exporting them
  - Bigger `batch_size`s are likely faster, but do consume more memory
  """
  await ocr.serialize_datasets(path, datasets(core, batch_size))