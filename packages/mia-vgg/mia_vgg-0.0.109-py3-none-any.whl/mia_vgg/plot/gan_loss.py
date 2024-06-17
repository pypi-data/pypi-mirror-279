import pickle
import matplotlib.pyplot as plt
import matplotlib
from pathlib import Path
import os
import sys

def plot(task):
    font = {'family' : 'serif',
            'weight' : 'normal',
            'size'   : 18}
    matplotlib.rc('font', **font)
    color = {"d":"blue",
             "g":"orange",
             }
    lab = {"d":"Discriminator",
           "g":"Generator",
           }
    for fold in range(5):
        for dtype in ["d", "g"]:
            path = Path("result", str(task), "gan", str(fold), f"{dtype.upper()}_losses.pickle")
            with open(path, "rb") as f:
                loss = pickle.load(f)
            if fold == 0:
                plt.plot(loss, color[dtype], label=lab[dtype])
            else:
                plt.plot(loss, color[dtype])
    plt.legend()
    plt.ylabel("Loss")
    plt.xlabel("SGD step")
    save_path = Path("plot", "loss")
    os.makedirs(save_path, exist_ok=True)
    save_path = Path(save_path, "gan_loss.pdf")
    plt.savefig(save_path, bbox_inches="tight")

if __name__=="__main__":
    task = sys.argv[1]
    plot(task)
