#!/usr/bin/env python3

import os
import sys
import click
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

from utils import load_communities
import numpy as np
import matplotlib.pyplot as plt



@click.command()
@click.argument('input', type=click.Path())
@click.argument('title', type=str)
def community_stats(input, title):
    communities = load_communities(input)

    print("Number of communities:", len(communities))

    lengths = [len(c) for c in communities]
    print("Mean size:", np.mean(lengths))
    print("Stddev size:", np.std(lengths))

    plt.hist(lengths, log=True)
    plt.xlabel('Size of Community')
    plt.ylabel('Frequency')
    plt.title(title)
    plt.show()

if __name__ == "__main__":
    community_stats()
