import argparse
import os
import shutil
import socket
import time

import torch
import torch.backends.cudnn as cudnn
import torch.nn as nn
import torch.nn.parallel
import torch.optim as optim
import torch.utils.data
import torchvision.utils as vutils
#from tensorboardX import SummaryWriter
from torch.autograd import Variable
from torch.optim.lr_scheduler import ReduceLROnPlateau
from torch.utils.data import DataLoader

import transformed as transforms
from data.ImageFolderDataset import MyImageFolder1
from models.HidingUNet import UnetGenerator
from models.RevealNet import RevealNet
import cv2
# from run import *
from video_crop_and_convert_to_frames import *
from video_from_frames import *
REVEALED_VIDEO_PATH=''
FINAL_SECRET_IMAGE_PATH='example_pics/final_secret_images/'
VIDEO_PATH=''
def rchop(thestring, ending):
	if thestring.endswith(ending):
		return thestring[:-len(ending)]
	return thestring
def weights_init(m):
    classname = m.__class__.__name__
    if classname.find('Conv') != -1:
        m.weight.data.normal_(0.0, 0.02)
    elif classname.find('BatchNorm') != -1:
        m.weight.data.normal_(1.0, 0.02)
        m.bias.data.fill_(0)

def rev(container_path):
	for the_file in os.listdir(FINAL_SECRET_IMAGE_PATH):
		os.remove(FINAL_SECRET_IMAGE_PATH+the_file)
	Rnet = RevealNet(output_function=nn.Sigmoid)
	# Rnet.cuda()
	Rnet.apply(weights_init)
	# if opt.Rnet != '':
	#     Rnet.load_state_dict(torch.load(opt.Rnet,map_location=lambda storage, loc: storage))
	# # if opt.ngpu > 1:
	#     Rnet = torch.nn.DataParallel(Rnet).cuda()
	# print_network(Rnet)
	
	criterion = nn.MSELoss()
	Rnet.eval()
	Rlosses = AverageMeter()
	container_test_dir="./example_pics/"+container_path
	test_dataset = MyImageFolder1(
            container_test_dir, 
            transforms.Compose([ 
                transforms.Resize([256, 256]),  
                transforms.ToTensor(),
            ]))
	assert test_dataset
	test_loader = DataLoader(test_dataset)
	for i, data in enumerate(test_loader, 0):
	# for data in TEST_LIST:	
		Rnet.zero_grad()
		container_img=data
		# print(data)
		# this_batch_size = int(container_img.size()[0])
		# containerFrames = container_img.resize_(this_batch_size, 3, 256, 256)
		# container_imgv = Variable(container_img, volatile=True)
		
		rev_secret_img = Rnet(container_img)
		RevSecImg=rev_secret_img.data
		# revSecFrames = RevSecImg.resize_(this_batch_size, 3, 256, 256)
		RSecImgName='%s/frame%03d.png'%(FINAL_SECRET_IMAGE_PATH,i)
		vutils.save_image(RevSecImg, RSecImgName, padding=1, normalize=True)


class AverageMeter(object):
    """
    Computes and stores the average and current value.
    """

    def __init__(self):
        self.reset()

    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count

def revealvideo(container_video_path):
	global REVEALED_VIDEO_PATH
	if(container_video_path.endswith("_container_video.avi")):
		reveal_video_path=rchop(container_video_path,"_container_video.avi")+"_secret_video.avi"
		# if(os.path.exists(reveal_video_path)):
		REVEALED_VIDEO_PATH= reveal_video_path
		print(REVEALED_VIDEO_PATH)
	else:
		# print("hi"+container_video_path)
		reveal_video_path=rchop(container_video_path,".avi")+"_secret_video.avi"
		convert_to_frames2(container_video_path)
		rev("container_images2")
		convert_frames_to_video(FINAL_SECRET_IMG_PATH,reveal_video_path)
		# reveal_video_path=VIDEO_PATH+container_video_path.slice(".avi")+"_reveal_video.avi"
		# global REVEALED_VIDEO_PATH
		REVEALED_VIDEO_PATH=reveal_video_path
		print(REVEALED_VIDEO_PATH)

def ret_revealed_video_path():
	global REVEALED_VIDEO_PATH
	return REVEALED_VIDEO_PATH

