from typing import TypedDict

class HParams(TypedDict):
  learning_rate: float
  weight_decay: float
  batch_size: int