import pickle
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from tqdm import tqdm
import numpy as np
import os
import sys

from .mia import shuffle, split

def aia(fold, dtype, sensitive):
    with open(Path("result", str(task), "target", dtype, str(fold), str(sensitive), "aia.pickle"), 'rb') as f:
        data = pickle.load(f)
    data = shuffle(data)
    ba = []
    for k in range(5):
        train, test = split(data)
        clf = RandomForestClassifier()
        clf.fit(train["soft"], train["s"])

        s_hat = clf.predict(test["soft"])
        s = test["s"]
        balanced_accuracy = np.mean([np.mean(s_hat[s==ss]==ss) for ss in np.unique(s)])
        ba += [balanced_accuracy]
    return ba

if __name__=="__main__":
    task = int(sys.argv[1])
    sensitive = int(sys.argv[2])
    
    path = Path("result", str(task), "aia", str(sensitive))
    #for dtype in ["real", "synth"]:
    for dtype in ["real"]:
        ba = []
        for fold in tqdm(range(1)):
            for k in range(1):
                ba += aia(fold, dtype, sensitive)
        os.makedirs(Path(path, dtype), exist_ok=True)
        with open(Path(path, dtype, "balanced_accuracy.pickle"), 'wb') as f:
            pickle.dump(ba, f)
