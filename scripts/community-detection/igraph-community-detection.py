#!/usr/bin/env python3

import click
import leidenalg
from igraph import *

@click.command()
@click.argument('input', type=click.Path())
@click.argument('output', type=click.Path())
def community_detection(input, output):
    print("Loading graph...")
    graph = Graph.Read_Pickle(input)

    print("Partitioning...")
    part = leidenalg.find_partition(graph, leidenalg.ModularityVertexPartition)

    print("Saving partition...")
    with open(output, "w") as file:
        for partition in part:
            file.write(repr(partition))
            file.write("\n")

if __name__ == "__main__":
    community_detection()
