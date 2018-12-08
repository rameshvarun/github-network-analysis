#!/usr/bin/env python3
from utils import load_communities
import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    communities = load_communities("results/communities.txt")

    print("Number of communities:", len(communities))

    lengths = [len(c) for c in communities]
    print("Mean size:", np.mean(lengths))
    print("Stddev size:", np.std(lengths))

    plt.hist(lengths, log=True)
    plt.xlabel('Size of Community')
    plt.ylabel('Frequency')
    plt.title("Leiden Algorithm Community Detection")
    plt.show()
