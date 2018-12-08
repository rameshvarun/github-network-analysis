#!/usr/bin/env python3
import snap

if __name__ == "__main__":
    print("Loading graph...")
    FIn = snap.TFIn("results/snap-follow.graph")
    graph = snap.TNGraph.Load(FIn)

    ugraph = snap.ConvertGraph(snap.PUNGraph, graph)

    print("Performing community detection...")
    CmtyV = snap.TCnComV()
    modularity = snap.CommunityCNM(ugraph, CmtyV)
    print("Modularity:", modularity)

    with open("results/communities.txt", "w") as file:
        for Cmty in CmtyV:
            file.write(repr([NI for NI in Cmty]))
            file.write("\n")
