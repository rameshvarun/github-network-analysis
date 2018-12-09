#!/usr/bin/env python2

import snap
import click

@click.command()
@click.argument('input', type=click.Path())
def clustering_coefficient(input):
    print("Loading graph...")
    FIn = snap.TFIn(input)
    graph = snap.TNGraph.Load(FIn)

    print("Calculating clustering coefficient...")
    print ("Clustering Coefficient:", snap.GetClustCf (graph, -1))

if __name__ == "__main__":
    clustering_coefficient()
