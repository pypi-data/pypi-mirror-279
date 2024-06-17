from typing import TextIO
from time import time
import keras
import tensorflow as tf
import demetric as dm
from checkptr import Checkpointer
from .steps import compile_train, compile_val

def finetune(
  model: keras.Model, train_ds: tf.data.Dataset, *,
  val_ds: tf.data.Dataset, opt: keras.optimizers.Optimizer,
  logger: dm.Metrics, checkpt: Checkpointer, logstream: TextIO,
  metrics_freq: int = 10, num_batches: int | None = None
):
  
  train_step = compile_train(model, opt)
  evaluate, metrics_step = compile_val(model)

  running_loss = 0.
  t0 = time()
  i = 0
  n = 0
  history: list[dict[str, float]] = []

  for epoch in range(10):
    t_epoch = time()
    for i, (x, y) in enumerate(train_ds):
      losses, z = train_step((x, y))
      loss = tf.reduce_mean(losses)
      running_loss += loss

      if i % metrics_freq == 0:
        t1 = time()
        batch_time = (t1-t0) / metrics_freq
        t0 = t1

        batch_metrics = metrics_step(y, z)
        display = ' - '.join([f'{k}: {v:.3f}' for k, v in batch_metrics.items()])
        msg = f'epoch {epoch} - {i} / {num_batches or "UNK"} - loss {float(loss):.3f} - {1e3*batch_time:.1f} ms/batch - {t1-t_epoch:.1f} secs elapsed - {display}'
        print(f'\r{msg}\t\t', end='', file=logstream, flush=True)

        step = n + i
        logger.log({'loss': float(loss), **batch_metrics}, step=step)

      if tf.math.is_nan(loss):
        print(f'WARNING: Loss is NaN at {i}', file=logstream)

    checkpt.checkpoint(model, f'{epoch}.weights.h5')
    val_metrics = evaluate(val_ds)
    val_metrics = { f'val_{k}': v for k, v in val_metrics.items() }
    history.append(val_metrics)
    logger.log(val_metrics, step=epoch)
    display = ' - '.join([f'{k}: {v:.3f}' for k, v in val_metrics.items()])
    print(f'\nValidation: {display}', file=logstream)

    n += i

  return history