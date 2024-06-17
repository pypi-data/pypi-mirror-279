from typing import Sequence
import keras
import tensorflow as tf
import tf.records as tfr
import moveread_ocr as mo

def parse_batch(x, char2num: keras.layers.StringLookup):
  return x['image'], mo.records.parse_labels(x['label'], char2num, vocab=mo.VOCABULARY)

def read_dataset(paths: Sequence[str], *, batch_size: int, char2num) -> tf.data.Dataset:
  return tfr.batched_read(
    mo.records.SCHEMA, paths, compression='GZIP',
    keep_order=False, batch_size=batch_size,
  ) \
  .map(lambda x: parse_batch(x, char2num)) \
  .prefetch(tf.data.AUTOTUNE) \
  .cache()
