import argparse

import torch

from model import Glow
from samplers import sample_data
from utils import net_args, calc_loss

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
N_DIM = 1

parser = net_args(argparse.ArgumentParser(description='Glow trainer'))
parser.add_argument('model_path', type=str,
                    help='path to model weights')
parser.add_argument('path', metavar='PATH', type=str, help='Path to image directory')

def test(args, model):
    dataset = iter(sample_data(args.path, args.batch * 10, args.img_size))
    model.eval()
    n_bins = 2. ** args.n_bits
    f = open(f'./test/ll_{str(args.delta)}_.txt', 'w')
    for i in range(100):
        with torch.no_grad():
            image_original, y = next(dataset)
            for cls in range(10):
                image = image_original[y == cls]
                print(image.shape)
                image = image.to(device)
                log_p, logdet, _ = model(image + torch.randn_like(image) * args.delta)
                logdet = logdet.mean()
                loss, log_p, log_det = calc_loss(log_p, logdet, args.img_size, n_bins)
                print(args.delta, log_p.item(), log_det.item(), cls, file=f)
    f.close()


if __name__ == '__main__':
    args = parser.parse_args()
    print(args)

    model_single = Glow(
        N_DIM, args.n_flow, args.n_block, affine=args.affine, conv_lu=not args.no_lu
    )
    model = model_single
    model.load_state_dict(torch.load(args.model_path))
    model = model.to(device)

    test(args, model)