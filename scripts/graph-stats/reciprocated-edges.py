import snap

if __name__ == "__main__":
    print("Loading graph...")
    FIn = snap.TFIn("results/snap-follow.graph")
    graph = snap.TNGraph.Load(FIn)


    bidirectional = snap.CntUniqBiDirEdges (graph)
    print ("Bidirectional Edges:", bidirectional)
    print ("Total Edges:", graph.GetEdges())

    print ("Reciprocated Ratio:", float(bidirectional) / graph.GetEdges())
