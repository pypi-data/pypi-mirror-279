from typing import Literal
import keras
import tensorflow as tf
import tf.records as tfr
import moveread_ocr as mo

def parse_batch(x, char2num: keras.layers.StringLookup):
  return x['image'], mo.records.parse_labels(x['label'], char2num, vocab=mo.VOCABULARY)

def read_dataset(
  path: str, *, batch_size: int, char2num,
  mode: Literal['shuffle', 'keep_order']
):
  data = tfr.Dataset.read(path)
  ds = data.iterate(mode=mode, batch_size=batch_size) \
    .map(lambda x: parse_batch(x, char2num)) \
    .prefetch(tf.data.AUTOTUNE) \
    .cache()
  
  return ds, data.len()
