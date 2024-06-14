"""Calculate FID and Inception Score of images in a directory."""

import argparse
import os
import tempfile

import torch
from torch.utils.data import DataLoader
from torch.utils.data.distributed import DistributedSampler

from .districuted import init, print0
from . import ImageDataset, get_inception_score_and_fid


def main(init_method, world_size, rank, args):
    init(init_method, world_size, rank)
    dataset = ImageDataset(root=args.path, num_images=args.num_images)
    sampler = DistributedSampler(dataset, shuffle=False)
    loader = DataLoader(
        dataset,
        batch_size=50,
        sampler=sampler,
        num_workers=args.num_workers)
    (IS, IS_std), FID = get_inception_score_and_fid(
        loader,
        args.stats,
        use_torch=args.use_torch,
        verbose=True)
    print0(IS, IS_std, FID)


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Calculate Inception Score and FID")
    parser.add_argument('--path', type=str, required=True,
                        help='path to image directory')
    parser.add_argument('--stats', type=str, required=True,
                        help='precalculated reference statistics')
    parser.add_argument('--use_torch', action='store_true',
                        help='using pytorch as the matrix operations backend')
    parser.add_argument("--num_images", type=int, default=None,
                        help="the number of images to calculate FID")
    parser.add_argument("--num_workers", type=int, default=4,
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
