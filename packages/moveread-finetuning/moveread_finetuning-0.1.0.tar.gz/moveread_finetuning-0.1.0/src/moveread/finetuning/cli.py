def main():
  from argparse import ArgumentParser
  
  parser = ArgumentParser('Moveread Round Finetuning')

  parser.add_argument('--train', type=str, required=True)
  parser.add_argument('--val', type=str, required=True)
  parser.add_argument('--weights', type=str, required=True)
  parser.add_argument('--base-path', type=str, required=True)

  parser.add_argument('--metrics-freq', type=int, default=10)

  parser.add_argument('--batch-size', type=int, default=32)
  parser.add_argument('--learning-rate', type=float, default=5e-4)
  parser.add_argument('--weight-decay', type=float, default=0.02)

  args = parser.parse_args()
  
  import sys
  from moveread.finetuning import run_finetuning
  
  run_finetuning(
    train=args.train, val=args.val, weights=args.weights,
    base_path=args.base_path, logstream=sys.stdout,
    batch_size=args.batch_size, learning_rate=args.learning_rate,
    weight_decay=args.weight_decay, metrics_freq=args.metrics_freq
  )
