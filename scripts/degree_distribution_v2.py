import snap
import numpy as np
import matplotlib.pyplot as plt

# Pruned
print("Loading graph...")
#FIn = snap.TFIn("../../GithubNetworkAnalysis/results/snap-follow-pruned.graph")
FIn = snap.TFIn("pr_v1.graph")
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
plt.loglog(X, Y, color = 'r', label = 'GitHub User-PR Network')
plt.xlabel('Node Degree (log)')
plt.ylabel('Proportion of Nodes with a Given Degree (log)')
plt.title('Degree Distribution of GitHub User-PR Network')
plt.legend()
plt.show()


# Now do in and out degree counts
# On pruned

# In
X, Y = [], []
DegToCntV = snap.TIntPrV()
snap.GetInDegCnt(graph, DegToCntV)
for item in DegToCntV:
    Y.append(item.GetVal2())
    X.append(item.GetVal1())

# Need proportion
total = float(sum(Y))
Y = [y / total for y in Y]

# Now plot it
plt.loglog(X, Y, color = 'r', label = 'GitHub User-PR Network - In Degree')

# Out
X, Y = [], []
DegToCntV = snap.TIntPrV()
snap.GetOutDegCnt(graph, DegToCntV)
for item in DegToCntV:
    Y.append(item.GetVal2())
    X.append(item.GetVal1())

# Need proportion
total = float(sum(Y))
Y = [y / total for y in Y]

# Now plot it
plt.loglog(X, Y, color = 'y', label = 'GitHub User-PR Network - Out Degree')

# All plotting
plt.xlabel('Node Degree (log)')
plt.ylabel('Proportion of Nodes with a Given Degree (log)')
plt.title('Degree Distribution of GitHub User-PR Network')
plt.legend()
plt.show()