import snap
import numpy as np
import matplotlib.pyplot as plt

print("Loading graph...")
FIn = snap.TFIn("../../GithubNetworkAnalysis/results/snap-follow.graph")
graph = snap.TNGraph.Load(FIn)

X, Y = [], []
DegToCntV = snap.TIntPrV()
snap.GetDegCnt(graph, DegToCntV)
for item in DegToCntV:
    Y.append(item.GetVal2())
    X.append(item.GetVal1())

# Need proportion
total = float(sum(Y))
Y = [y / total for y in Y]

# Now plot it
plt.loglog(X, Y, color = 'y', label = 'GitHub Network')
plt.xlabel('Node Degree (log)')
plt.ylabel('Proportion of Nodes with a Given Degree (log)')
plt.title('Degree Distribution of GitHub Network')
plt.legend()
plt.show()