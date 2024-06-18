import pickle
import csv
from torchvision.datasets import VisionDataset
from pathlib import Path
import os
import PIL
import numpy as np
import torch

class SyntheticCeleba(VisionDataset):
    def __init__(self, root, target_transform=None, transform=None, no_lab=False):
        super().__init__(root, transform=transform, target_transform=target_transform)
        self._load_filename()

    def _load_filename(self):
        path = Path(self.root)
        self.filename = []
        self.attr = []
        with open(Path(path, "attribute.csv")) as f:
            reader = csv.reader(f, delimiter=",")
            for row in reader:
                self.filename += [row[0]]
                self.attr += [int(float(row[1]))]

    def __getitem__(self, index):
        X = PIL.Image.open(Path(self.root, 
                                "images", 
                                self.filename[index]))
        if self.transform is not None:
            X = self.transform(X)
        target = torch.tensor(self.attr[index]).type(torch.LongTensor)
        if self.target_transform is not None:
            target = self.target_transform(target)

        return X, target

    def __len__(self):
        return len(self.filename)
