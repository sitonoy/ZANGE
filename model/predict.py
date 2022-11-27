import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
from torchvision import transforms
import pytorch_lightning as pl
from torchvision.models import resnet18



def transform(img):
  transform_ = transforms.Compose([
                                transforms.ToTensor(),
                                transforms.Resize(256),
                                transforms.CenterCrop(224),
                                transforms.Normalize(mean=[0.485,0.456,0.406],std=[0.229,0.224,0.225])
  ])
  img_ = transform_(img)
  return img_

class Net(pl.LightningModule):
  def __init__(self):
    super().__init__()
    self.feature = resnet18(pretrained = False)
    self.fc = nn.Linear(1000,2)
  
  def forward(self,x):
    h = self.feature(x)
    h = self.fc(h)
    return h
  