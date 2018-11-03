import snap

if __name__ == "__main__":
    print("Loading graph...")
    FIn = snap.TFIn("results/snap-follow.graph")
    graph = snap.TNGraph.Load(FIn)

    print("Calculating clustering coefficient...")
    print ("Clustering Coefficient:", snap.GetClustCf (graph, -1))
