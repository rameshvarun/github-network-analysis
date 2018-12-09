#!/usr/bin/env python3

from igraph import *

from utils import cached

@cached('results/maximal-cliques.pickle')
def get_cliques():
    print("Loading graph...")
    graph = Graph.Read_Pickle('results/igraph-follow-pruned.pickle')

    print("Finding maximal cliques...")
    return graph.maximal_cliques()

if __name__ == '__main__':
    cliques = get_cliques()
    print(cliques)
