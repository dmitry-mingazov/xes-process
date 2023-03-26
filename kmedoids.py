#!/usr/bin/env python3.10
from collections import defaultdict
from pathlib import Path
import pandas as pd
from sklearn_extra.cluster import KMedoids
import numpy as np
from datetime import datetime
from sklearn import metrics

import matplotlib.pyplot as plt

import sys

def kmedoids_clustering(path, n, output_dir):
    # OUTPUT_PATH = Path(f"_clustering_{datetime.now().strftime('%d_%b_%H_%M_%S')}")
    # n = int(sys.argv[2])
    # n = int(n/2)
    # path = str(sys.argv[1])
    dm = pd.read_csv(path, delimiter=',')
    df1 = dm.iloc[:, 1:]
    dm = dm.iloc[:, 1:]

    df1 = df1.to_records(index=False)
    df1 = df1.tolist()
    df1 = np.array(df1, dtype=object)

    # k_max = 0
    best_clusterization = dict(
        silhouette=-1,
        k=0,
        labels=[]
    )
    silhouettes = []
    for k in range(2, n):
        # with open("./log_new_kmedoid", mode="a") as f:
            # f.write(f"[{datetime.now()}] - k:{k} started\n")

        kmedoids_instance = KMedoids(n_clusters=k, metric="precomputed", 
                                     method="pam", init="build", 
                                     max_iter=300, random_state=1).fit(df1)
        if (all(kmedoids_instance.labels_ == 0)):
            silhouettes.append(0)
            continue
        score = metrics.silhouette_score(df1, kmedoids_instance.labels_, metric="precomputed")
        silhouettes.append(score)
        if score > best_clusterization.get('silhouette', -1):
            best_clusterization['silhouette'] = score
            best_clusterization['k'] = k
            best_clusterization['labels'] = kmedoids_instance.labels_
        # with open("./log_new_kmedoid", mode="a") as f:
            # f.write(f"Silhoutte {score}\n")
            # f.write(f"[{datetime.now()}] - k:{k} ended\n")

    plt.plot(silhouettes)
    plt.savefig(output_dir / "silhouette_plot.png")

    # save silhouettes on file
    with open(output_dir / "silhouettes.txt", mode="w") as f:
        f.write(f"k: {best_clusterization['k']} - silhouette = {best_clusterization['silhouette']}\n")
        for index, silhouette in enumerate(silhouettes):
            # silhouettes are saved from 2 to 'n'
            f.write(f"{index+2}: {silhouette}\n")

    res = defaultdict(list)
    with open(output_dir / "kmedoids_clustering.csv", mode="w") as f:
        # f.write(f"k: {best_clusterization['k']} - silhouette = {best_clusterization['silhouette']}\n")
        f.write("NomeLog,ClusterId,\n")
        for index, label in enumerate(best_clusterization['labels']):
            # res[dm.columns[index]].append(label)
            res[label].append(dm.columns[index])
            f.write(f"{dm.columns[index]},{label},\n")
    return res

if __name__ == "__main__":
    kmedoids_clustering(sys.argv[1], int(sys.argv[2]), Path(sys.argv[3]))