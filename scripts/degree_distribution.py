import snap
import numpy as np
import matplotlib.pyplot as plt

'''
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
plt.loglog(X, Y, color = 'y', label = 'GitHub Network - Original')

# Pruned
print("Loading graph...")
FIn = snap.TFIn("../../GithubNetworkAnalysis/results/snap-follow-pruned.graph")
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
plt.loglog(X, Y, color = 'b', label = 'GitHub Network - Pruned')
plt.xlabel('Node Degree (log)')
plt.ylabel('Proportion of Nodes with a Given Degree (log)')
plt.title('Degree Distribution of GitHub Network')
plt.legend()
plt.show()
'''

# Now do in and out degree counts
print("Loading graph...")
FIn = snap.TFIn("../../GithubNetworkAnalysis/results/snap-follow.graph")
graph = snap.TNGraph.Load(FIn)

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
plt.loglog(X, Y, color = 'y', label = 'GitHub Network - Original In Degree')

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
plt.loglog(X, Y, color = 'r', label = 'GitHub Network - Original Out Degree')

# On pruned
print("Loading graph...")
FIn = snap.TFIn("../../GithubNetworkAnalysis/results/snap-follow-pruned.graph")
graph = snap.TNGraph.Load(FIn)

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
plt.loglog(X, Y, color = 'b', label = 'GitHub Network - Pruned In Degree')

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
plt.loglog(X, Y, color = 'g', label = 'GitHub Network - Pruned Out Degree')

# All plotting
plt.xlabel('Node Degree (log)')
plt.ylabel('Proportion of Nodes with a Given Degree (log)')
plt.title('Degree Distribution of GitHub Network')
plt.legend()
plt.show()