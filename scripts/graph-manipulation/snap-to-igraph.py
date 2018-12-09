#!/usr/bin/env python2
import snap
import igraph
import click

@click.command()
@click.argument('input', type=click.Path())
@click.argument('output', type=click.Path())
def snap_to_igraph(input, output):
    print("Loading graph...")
    FIn = snap.TFIn(input)
    graph = snap.TNGraph.Load(FIn)

    conv_graph = igraph.Graph(directed=True)
    conv_graph.add_vertices(str(node.GetId()) for node in graph.Nodes())
    conv_graph.add_edges((str(e.GetSrcNId()), str(e.GetDstNId())) for e in graph.Edges())

    conv_graph.write_pickle(output)

if __name__ == "__main__":
    snap_to_igraph()
