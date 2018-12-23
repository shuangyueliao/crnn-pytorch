import os
import cv2
import string
import click
import torch
from torch.autograd import Variable
import json
from models.model_loader import load_model


def singleOp(net, img, cuda, visualize):
    img = torch.from_numpy(img.transpose((2, 0, 1))).float()
    img = torch.unsqueeze(img, 0)
    img = Variable(img)
    if cuda:
        img = img.cuda()
    out = net(img, decode=True)
    return out

@click.command()
@click.option('--data-path', type=str, default='d', help='Path to dataset')
@click.option('--abc', type=str, default=string.digits+string.ascii_uppercase, help='Alphabet')
@click.option('--seq-proj', type=str, default="10x20", help='Projection of sequence')
@click.option('--backend', type=str, default="resnet18", help='Backend network')
@click.option('--snapshot', type=str, default='e/crnn_resnet18_0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_best', help='Pre-trained weights')
@click.option('--input-size', type=str, default="320x32", help='Input size')
@click.option('--gpu', type=str, default='0', help='List of GPUs for parallel training, e.g. 0,1,2,3')
@click.option('--visualize', type=bool, default=False, help='Visualize output')
def main(data_path, abc, seq_proj, backend, snapshot, input_size, gpu, visualize):
    os.environ["CUDA_VISIBLE_DEVICES"] = gpu
    cuda = True if gpu is not '' else False

    input_size = [int(x) for x in input_size.split('x')]
    seq_proj = [int(x) for x in seq_proj.split('x')]
    config = json.load(open(os.path.join(data_path, "desc.json")))
    net = load_model(config["abc"], seq_proj, backend, snapshot, cuda).eval()
    
    DEBUG = True
    if DEBUG:
        img = cv2.imread('2.png')
        img = cv2.resize(img, (input_size[0], input_size[1]))
        out = singleOp(net, img, cuda, visualize)
        print(out[0])
        return
        
    files = os.listdir('./d/data')
    tongji = 0
    for myfile in files:
        img = cv2.imread('./d/data/' + myfile)
        img = cv2.resize(img, (input_size[0], input_size[1]))
        out = singleOp(net, img, cuda, visualize)
        splits = myfile.split('_')
        id=splits[0]
        if splits[-1]=='0.jpg':
            trueresult = id[:len(id)//2-1]
        else:
            trueresult = id[len(id)//2:]      
        if trueresult == out[0]:
            tongji += 1
        else:
            print(myfile)
            print(out)
            print(trueresult)
            print('--------------------')
    print(tongji*1.0 / len(files))

if __name__ == '__main__':
    main()
