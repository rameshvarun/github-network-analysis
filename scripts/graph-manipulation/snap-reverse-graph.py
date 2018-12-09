#!/usr/bin/env python2
import snap
import click

@click.command()
@click.argument('input', type=click.Path())
@click.argument('output', type=click.Path())
def reverse_graph(input, output):
    print("Loading graph...")
    FIn = snap.TFIn(input)
    graph = snap.TNGraph.Load(FIn)

    reversed_graph = snap.TNGraph.New()
    for node in graph.Nodes():
        reversed_graph.AddNode(node.GetId())

    for e in graph.Edges():
        reversed_graph.AddEdge(e.GetDstNId(), e.GetSrcNId())

    assert graph.GetNodes() == reversed_graph.GetNodes()
    assert graph.GetEdges() == reversed_graph.GetEdges()

    FOut = snap.TFOut(output)
    reversed_graph.Save(FOut)
    FOut.Flush()

if __name__ == "__main__":
    reverse_graph()
