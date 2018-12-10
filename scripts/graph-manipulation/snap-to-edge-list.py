#!/usr/bin/env python2
import snap
import click

@click.command()
@click.argument('input', type=click.Path())
@click.argument('output', type=click.Path())
def snap_to_edge_list(input, output):
    print("Loading graph...")
    FIn = snap.TFIn(input)
    graph = snap.TNGraph.Load(FIn)
    snap.SaveEdgeList(graph, output)

if __name__ == "__main__":
    snap_to_edge_list()
