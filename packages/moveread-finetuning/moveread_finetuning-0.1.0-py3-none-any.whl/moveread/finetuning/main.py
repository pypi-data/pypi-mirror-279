from typing import TypedDict, Unpack, TextIO
from glob import glob
import os
import json
from haskellian import iter as I
import numpy as np
import keras
import demetric as dm
from checkptr import Checkpointer
from .model import load_model
from .data import read_dataset
from .loop import finetune

class HParams(TypedDict):
  learning_rate: float
  weight_decay: float
  batch_size: int

def load_data(train: str, val: str, *, batch_size: int, char2num):
  train_ds = read_dataset(glob(train), batch_size=batch_size, char2num=char2num).shuffle(100)
  val_ds = read_dataset(glob(val), batch_size=batch_size, char2num=char2num)
  return train_ds, val_ds

def create_run(base_path: str, hparams: HParams):
  logger = dm.Metrics.new(os.path.join(base_path, 'metrics'), overwrite=True)
  checkpt = Checkpointer.keras(os.path.join(base_path, 'checkpoints'))
  with open(os.path.join(base_path, 'hparams.json'), 'w') as f:
    json.dump(hparams, f, indent=2)

  return logger, checkpt

def run_finetuning(
  *, train: str, val: str, weights: str, base_path: str,
  logstream: TextIO, metrics_freq: int = 10, **hparams: Unpack[HParams]
):
  
  print('Loading model...', file=logstream)
  model, char2num, _ = load_model(weights)
  
  print('Loading datasets...', file=logstream)
  train_ds, val_ds = load_data(train, val, batch_size=hparams['batch_size'], char2num=char2num)

  opt = keras.optimizers.Adam(learning_rate=hparams['learning_rate'], weight_decay=hparams['weight_decay'])
  
  print(f'Creating run at "{base_path}"...', file=logstream)
  logger, checkpt = create_run(base_path, hparams)
  print('Starting finetuning...', file=logstream)
  history = finetune(model, train_ds, val_ds=val_ds, opt=opt, logger=logger, checkpt=checkpt, logstream=logstream, metrics_freq=metrics_freq)
  print('Training finished')
  
  for metric in history[0].keys():
    metrics = list(I.pluck(history, metric))
    best_epoch: int = np.argmax(metrics) if 'accuracy' in metric else np.argmin(metrics) # type: ignore
    print(f'Best {metric} at epoch {best_epoch}: {metrics[best_epoch]}', file=logstream)