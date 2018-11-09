import snap
import numpy as np
import matplotlib.pyplot as plt
import operator

# Helper to compute all the features
def getFeatureVecBasic(G, nid):
	node = G.GetNI(nid)
	feat1 = node.GetDeg()

	# Now get egonet
	ego = snap.TUNGraph()
	ego.AddNode(node.GetId())

	# Add all of the neighbors and edge to node
	Nbrs = snap.TIntV()
	snap.GetCmnNbrs(G, nid, nid, Nbrs)
	Nbrs.Add(nid)
	feat2, feat3 = snap.GetEdgesInOut(G, Nbrs)
	
	# Return the vec
	return np.array([feat1, feat2, feat3])

# Helper for cosine sim
def cosineSim(x, y):
	normx = np.linalg.norm(x)
	normy = np.linalg.norm(y)
	if normx == 0 or normy == 0:
		return 0
	return np.dot(x, y) / (normx * normy)

def q1_1():
	FIn = snap.TFIn("../../GithubNetworkAnalysis/results/snap-follow-pruned.graph")
	G = snap.TNGraph.Load(FIn)

	# Run for 9
	result1 = getFeatureVecBasic(G, 9)
	print 'Basic feature vector for node 9', result1

	# Find most similar
	sims = {}
	for node in G.Nodes():
		sims[node.GetId()] = cosineSim(result1, getFeatureVecBasic(G, node.GetId()))

	# Sort https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value
	sorted_sims = sorted(sims.items(), key=operator.itemgetter(1), reverse=True)
	print 'Sorted by similarity', sorted_sims[:7]

# Helper to run recursive for some k on g
def runRecursive(G, k=2):
	dicts = [{} for i in range(k+1)]
	
	# Now for each iteration, we keep going
	for i in range(k+1):
		# Handle base case separately
		if i == 0:
			for node in G.Nodes():
				dicts[0][node.GetId()] = getFeatureVecBasic(G, node.GetId())

		# Otherwise, we do it the normal way
		else:
			for node in G.Nodes():
				# Get all of the neighbors of our node
				Nbrs = snap.TIntV()
				snap.GetCmnNbrs(G, node.GetId(), node.GetId(), Nbrs)
				sumVec = np.zeros(3**(i))

				# For each neighbor, get mean and sum
				for nbr in Nbrs:
					sumVec += dicts[i-1][nbr]

				# Handle edge case
				meanVec = None
				if len(Nbrs) == 0:
					meanVec = np.zeros(3**(i))
				else:
					meanVec = sumVec / float(len(Nbrs))

				# Now concatenate
				dicts[i][node.GetId()] = np.concatenate((dicts[i-1][node.GetId()], meanVec, sumVec))
	return dicts[-1]

def q1_2():
	G = snap.TUNGraph.Load(snap.TFIn("hw2-q1.graph"))

	# Use Helper
	last = runRecursive(G)

	# Find most similar
	sims = {}
	for node in G.Nodes():
		sims[node.GetId()] = cosineSim(last[9], last[node.GetId()])
	sorted_sims = sorted(sims.items(), key=operator.itemgetter(1), reverse=True)
	print 'Sorted by similarity', sorted_sims[:10]

def q1_3():
	G = snap.TUNGraph.Load(snap.TFIn("hw2-q1.graph"))

	# Use Helper
	last = runRecursive(G)

	# Find most similar
	sims = {}
	for node in G.Nodes():
		sims[node.GetId()] = cosineSim(last[9], last[node.GetId()])

	# Now we need to plot 20-bin histogram!
	# Each bin should contain 1/20 = 0.05 of room, so first is 0-0.05 last is 0.95-1.0
	'''
	xs = []
	bins = np.zeros(20)
	for key in sims.keys():
		bin = int(20 * sims[key])
		if bin == 20:
			#print 'HECCIN GOOD BOI'
			bin = 19
		bins[bin] += 1
		xs.append(sims[key])
	print bins

	plt.hist(xs, bins=50)
	plt.title('1.3 Histogram')
	plt.ylabel('Number of Nodes');
	plt.xlabel('Cosine Similiarity with Node 9');
	plt.show()
	'''

	# Get first group (0 similarity)
	# Just change this to a range every time we need new one
	vec = None
	keyID = None
	for key in sims.keys():
		#if sims[key] < 0.93 and sims[key] > 0.87:
		if sims[key] >= 0.6 and sims[key] <= 0.65:
			keyID = key
			vec = last[key]
	print keyID
	print vec


q1_1()
#q1_2()
#q1_3()



