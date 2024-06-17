from haskellian import dicts as D
import keras
import tensorflow as tf
from tf.tools import tf_function
import tf.ctc as ctc

def compile_train(model: keras.Model, opt: keras.Optimizer):
  @tf_function
  def train_step(batch):
    x, y = batch
    with tf.GradientTape() as tape:
      z = model(x, training=True)
      loss = tf.clip_by_value(ctc.loss(y, z), 0, 100) # clip to avoid NaNs, shouldn't get over 100 anyway

    grads = tape.gradient(loss, model.trainable_variables)
    opt.apply_gradients(zip(grads, model.trainable_variables)) # type: ignore (idk tbh)
    return loss, z
  
  return train_step

def compile_val(model: keras.Model):

  @tf_function
  def metrics_step(y, z):
    paths, _ = ctc.beam_decode(z, top_paths=25)
    return {
      'accuracy': ctc.preds_accuracy(y, paths[:1]),
      'edit_distance': tf.clip_by_value(ctc.preds_edit_distance(y, paths[:1]), 0, 100),
      'accuracy5': ctc.preds_accuracy(y, paths[:5]),
      'accuracy25': ctc.preds_accuracy(y, paths[:25]),
      'edit_distance5': tf.clip_by_value(ctc.preds_edit_distance(y, paths[:5]), 0, 100),
      'edit_distance25': tf.clip_by_value(ctc.preds_edit_distance(y, paths[:25]), 0, 100),
    }
  
  @tf_function
  def val_step(batch):
    x, y = batch
    z = model(x, training=False)
    return metrics_step(y, z) | {'loss': tf.reduce_mean(ctc.loss(y, z)) }
  
  def evaluate(val_ds: tf.data.Dataset):
    metrics = [val_step(batch) for batch in val_ds]
    avg = D.aggregate(tf.reduce_mean, metrics)
    return D.map_v(float, avg)
  
  return evaluate, metrics_step