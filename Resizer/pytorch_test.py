import torch
from torch.utils.data import Dataset
import pandas as pd
import traceback
import sys

def encode(points, padded_length = 100):
    input_tensor = torch.zeros([2, padded_length])
    for i in range(min(padded_length, len(points))):
        input_tensor[0][i] = points[i][0] * 1.0
        input_tensor[1][i] = points[i][1] * 1.0
        continue
    return input_tensor

"""Simple classifier structure
   the intention of this class was to be used on datasets
   with 32x32 png images less than 10 classes, easily modifiable though
"""

class Classifier(torch.nn.Module):
    def __init__(self, classes):
        super(Classifier, self).__init__()
        self.num_classes = len(classes)
        self.hidden_layer = torch.nn.Sequential(
                            torch.nn.Linear(32*32*4, 1000),
                            torch.nn.ReLU(0.2),
                            torch.nn.Sigmoid(),
                            torch.nn.Linear(1000, 250),
                            torch.nn.ReLU(),
                            torch.nn.Linear(250, 10),
                            torch.nn.Linear(10, self.num_classes)
        )

    def forward(self, x):
        x = self.hidden_layer(x)
        return x


""" Custom Dataset for csv datasets
    """
class Custom_Dataset(Dataset):
    """docstring for Custom Dataset."""
    def __init__(self, csv_file):
        super(Custom_Dataset, self).__init__()
        try:
            #this wrapper will rely on pandas to read the csv file, please
            # pip3 install pandas to use this code
            self.tabledf = pd.read_csv(csv_file)
        except IOError as e:
            print("Sorry that csv file does not exist")
            sys.exit(0)

    def __len__(self):
        return len(self.tabledf)

    def __getitem__(self, idx):
        return self.tabledf.loc[idx]


if __name__ == '__main__':
    #GET HYPERPARAMETERS#
    opt = pd.DataFrame()
    opt.lr = 1e-3
    opt.beta1=.5

    ds = Custom_Dataset('test_wrapper.csv')

    print(ds[0][0])

    classes = ['Malignant', 'Benign']
    c = Classifier(classes)
