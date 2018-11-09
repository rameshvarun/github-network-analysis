import snap
import numpy as np
import matplotlib.pyplot as plt

'''
print("Loading graph...")
FIn = snap.TFIn("../../GithubNetworkAnalysis/results/snap-follow.graph")
graph = snap.TNGraph.Load(FIn)

# Do 100 sample points for now

inward = []
for i in range(100):
    NId = graph.GetRndNId()
    InBfsTree = snap.GetBfsTree(graph, NId, False, True)
    inward.append(InBfsTree.GetNodes())
# sort
inwardY = sorted(inward)
inwardX = list(np.linspace(0,1,100,endpoint=False))

# Plot
plt.plot(inwardX, inwardY)
plt.xlabel('Fraction of Starting Nodes')
plt.ylabel('Number of Nodes Reached')
plt.title('Reachability using Inlinks - Original')
plt.legend()
plt.show()


# Outward email
outward = []
for i in range(100):
    NId = graph.GetRndNId()
    OutBfsTree = snap.GetBfsTree(graph, NId, True, False)
    outward.append(OutBfsTree.GetNodes())
# sort
outwardY = sorted(outward)
outwardX = list(np.linspace(0,1,100,endpoint=False))

# Plot
plt.plot(outwardX, outwardY)
plt.xlabel('Fraction of Starting Nodes')
plt.ylabel('Number of Nodes Reached')
plt.title('Reachability using Outlinks - Original')
plt.legend()
plt.show()
'''

# Now do pruned
print("Loading graph...")
FIn = snap.TFIn("../../GithubNetworkAnalysis/results/snap-follow-pruned.graph")
graph = snap.TNGraph.Load(FIn)

# Do 100 sample points for now
'''
inward = []
for i in range(100):
    NId = graph.GetRndNId()
    InBfsTree = snap.GetBfsTree(graph, NId, False, True)
    inward.append(InBfsTree.GetNodes())
# sort
inwardY = sorted(inward)
inwardX = list(np.linspace(0,1,100,endpoint=False))

# Plot
plt.plot(inwardX, inwardY)
plt.xlabel('Fraction of Starting Nodes')
plt.ylabel('Number of Nodes Reached')
plt.title('Reachability using Inlinks - Pruned')
plt.legend()
plt.show()
'''


# Outward 
outward = []
for i in range(100):
    NId = graph.GetRndNId()
    OutBfsTree = snap.GetBfsTree(graph, NId, True, False)
    outward.append(OutBfsTree.GetNodes())
# sort
outwardY = sorted(outward)
outwardX = list(np.linspace(0,1,100,endpoint=False))

# Plot
plt.plot(outwardX, outwardY)
plt.xlabel('Fraction of Starting Nodes')
plt.ylabel('Number of Nodes Reached')
plt.title('Reachability using Outlinks - Pruned')
plt.legend()
plt.show()