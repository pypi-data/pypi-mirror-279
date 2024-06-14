"""Calculate statistics for FID and save to a file."""

import argparse
import os
import tempfile

import torch

from .districuted import init
from .utils import calc_and_save_stats


def main(init_method, world_size, rank, args):
    init(init_method, world_size, rank)

    calc_and_save_stats(
        args.path,
        args.output,
        args.batch_size,
        args.img_size,
        args.use_torch,
        args.num_workers)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        "A handy cli tool to calculate FID statistics.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--path", type=str, required=True,
                        help='path to image directory (include subfolders)')
    parser.add_argument("--output", type=str, required=True,
                        help="output file path")
    parser.add_argument("--batch_size", type=int, default=50,
                        help="batch size")
    parser.add_argument("--img_size", type=int, default=None,
                        help="resize image to this size")
    parser.add_argument('--use_torch', action='store_true',
                        help='using pytorch as the matrix operations backend')
    parser.add_argument("--num_workers", type=int, default=os.cpu_count(),
                        help="dataloader workers")

    args = parser.parse_args()

    world_size = len(os.environ.get('CUDA_VISIBLE_DEVICES', "0").split(','))
    with tempfile.TemporaryDirectory() as temp:
        init_method = f'file://{os.path.abspath(os.path.join(temp, ".ddp"))}'
        processes = []
        for rank in range(world_size):
            p = torch.multiprocessing.Process(
                target=main,
                args=(init_method, world_size, rank, args))
            p.start()
            processes.append(p)
        for p in processes:
            p.join()
