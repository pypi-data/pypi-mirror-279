import keras
import moveread_ocr as mo

def load_model(weights: str):
  char2num = keras.layers.StringLookup(vocabulary=list(mo.VOCABULARY), num_oov_indices=1)
  num2char = keras.layers.StringLookup(vocabulary=char2num.get_vocabulary(), invert=True)
  size = len(char2num.get_vocabulary())
  base = mo.BaseCRNN(size)
  model = mo.AdaptedChessCRNN(base, size)
  model.load_weights(weights)
  return model, char2num, num2char