import argparse
import os
import time
from spleeter.separator import Separator


class Timer:
    def __enter__(self, *args):
        self.start = time.monotonic()
        return self
    
    def __exit__(self, *args):
        self.elapsed = time.monotonic() - self.start
        print(f'Done in {self.elapsed:.2f} seconds', flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--device', default="cpu")
    parser.add_argument('--output_dir', default='output')
    parser.add_argument('files', nargs='*')
    args = parser.parse_args()
    os.makedirs(args.output_dir, exist_ok=True)

    print('Setting up... ', end='')
    with Timer():
        separator = Separator('spleeter:4stems')
        #device = torch.device(args.device)  # optionally use the GPU
        #state = torch.load("best_model.pt", map_location=device)  # load checkpoint
        #network = MultiTasNet(state["args"]).to(device)  # initialize the model
        #network.load_state_dict(state['state_dict'])  # load weights from the checkpoint
    
    # print(args.files)
    for input_fn in args.files:
        # print(input_fn, flush=True)
        print(f'Separating {input_fn}... ', end='')
        with Timer():
            separator.separate_to_file(input_fn, args.output_dir)


if __name__ == '__main__':
    main()
