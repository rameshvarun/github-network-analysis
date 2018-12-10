#!/usr/bin/env python2
import snap
import click

@click.command()
@click.argument('input', type=click.Path())
@click.argument('output', type=click.Path())
def community_detection(input, output):
    print("Loading graph...")
    FIn = snap.TFIn(input)
    graph = snap.TNGraph.Load(FIn)

    ugraph = snap.ConvertGraph(snap.PUNGraph, graph)

    print("Performing community detection...")
    CmtyV = snap.TCnComV()
    modularity = snap.CommunityCNM(ugraph, CmtyV)
    print("Modularity:", modularity)

    with open(output, "w") as file:
        for Cmty in CmtyV:
            file.write(repr([NI for NI in Cmty]))
            file.write("\n")

if __name__ == "__main__":
    community_detection()
