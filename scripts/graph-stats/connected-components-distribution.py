import snap
import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    print("Loading graph...")
    FIn = snap.TFIn("results/snap-follow.graph")
    graph = snap.TNGraph.Load(FIn)

    print("Finding strongly connected components...")
    dist = snap.TIntPrV()
    snap.GetSccSzCnt(graph, dist)
    sccs = [(comp.GetVal1(), comp.GetVal2()) for comp in dist]

    print("Finding weakly connected components...")
    dist = snap.TIntPrV()
    snap.GetWccSzCnt(graph, dist)
    wccs = [(comp.GetVal1(), comp.GetVal2()) for comp in dist]

    print("Number of SCCs:", sum(scc[1] for scc in sccs))
    print("Number of WCCs:", sum(wcc[1] for wcc in wccs))

    plt.scatter([scc[0] for scc in sccs], [scc[1] for scc in sccs], s=4, label = 'WCC Distribution')
    plt.scatter([wcc[0] for wcc in wccs], [wcc[1] for wcc in wccs], s=4, label = 'SCC Distribution')

    plt.yscale('log')
    plt.xscale('log')

    plt.title('WCC / SCC Size Distribution')

    plt.xlabel('Component Size')
    plt.ylabel('Frequency')

    plt.legend()

    plt.show()
