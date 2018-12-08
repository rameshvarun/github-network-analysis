#!/usr/bin/env python3

import leidenalg
from igraph import *

if __name__ == '__main__':
    print("Loading graph...")
    graph = Graph.Read_Pickle('results/igraph-follow-pruned.pickle')

    print("Partitioning...")
    part = leidenalg.find_partition(graph, leidenalg.ModularityVertexPartition)

    print("Saving partition...")
    with open("results/communities.txt", "w") as file:
        for partition in part:
            file.write(repr(partition))
            file.write("\n")
