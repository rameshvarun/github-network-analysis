import snap
import numpy as np
import matplotlib.pyplot as plt
import operator
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import pickle

# Seed
Rnd = snap.TRnd(224)

# Helper to compute all the features
def getFeatureVecBasic(G, nid):
	node = G.GetNI(nid)
	feat1 = node.GetDeg()

	# Now get egonet
	ego = snap.TNGraph()
	ego.AddNode(node.GetId())

	# Add all of the neighbors and edge to node
	Nbrs = snap.TIntV()
	snap.GetNodesAtHop(G, nid, 1, Nbrs, True)
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

# Helper to run recursive for some k on g
def runRecursive(G, testNodes, k=2):
	dicts = [{} for i in range(k)]

	# Subset
	#print testNodes
	
	# Now for each iteration, we keep going
	for i in range(k):
		# Handle base case separately
		print "Feature level", i
		counter = 1
		if i == 0:
			for node in testNodes:
				print 'Node', counter
				counter += 1
				dicts[0][node] = getFeatureVecBasic(G, node)

				# Also need to get all of the neighbor feature vecs
				Nbrs = snap.TIntV()
				snap.GetNodesAtHop(G, node, 1, Nbrs, True)
				for nbr in Nbrs:
					dicts[0][nbr] = getFeatureVecBasic(G, nbr)

					# And for neighbors' neighbors
					NbrsNbrs = snap.TIntV()
					snap.GetNodesAtHop(G, nbr, 1, NbrsNbrs, True)
					for nbrnbr in NbrsNbrs:
						dicts[0][nbrnbr] = getFeatureVecBasic(G, nbrnbr)


		# Otherwise, we do it the normal way
		else:
			for node in testNodes:
				print 'Node', counter
				counter += 1
				# Get all of the neighbors of our node
				Nbrs = snap.TIntV()
				snap.GetNodesAtHop(G, node, 1, Nbrs, True)
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
				dicts[i][node] = np.concatenate((dicts[i-1][node], meanVec, sumVec))

		# Pickle to save
		with open('feats_' + str(i) + '_graph2.pkl', 'wb') as f:
			pickle.dump(dicts[i], f)

	return dicts[-1]

def run_recursive_feats():
	#FIn = snap.TFIn("../../GithubNetworkAnalysis/results/snap-follow-pruned.graph")
	FIn = snap.TFIn("pr_v1.graph")
	G = snap.TNGraph.Load(FIn)

	# Subset random test
	testNodes = [G.GetRndNId(Rnd) for i in range(1000)]

	# Use Helper
	print 'Estimating features'
	last = runRecursive(G, testNodes)
	print last

	# Save as pickle since this takes forever
	with open('recursive_features_graph2.pkl', 'wb') as f:
		pickle.dump(last, f)

	# Now do kmeans
	print 'Kmeans'
	clusters = []
	for item in last.itervalues():
		clusters.append(item)

	kmeans = KMeans(n_clusters=5, random_state=0).fit(clusters)
	print kmeans.cluster_centers_

	print 'PCA'
	pca = PCA(n_components=2)
	pca.fit(clusters)
	results = pca.transform(clusters)
	plt.scatter(results[:,0], results[:,1])
	plt.xlabel('First Principal Component')
	plt.ylabel('Second Principal Component')
	plt.title('RolX Algorithm Principal Components')
	plt.show()

	# Find most similar
	'''
	sims = {}
	for node in G.Nodes():
		sims[node.GetId()] = cosineSim(last[9], last[node.GetId()])
	sorted_sims = sorted(sims.items(), key=operator.itemgetter(1), reverse=True)
	print 'Sorted by similarity', sorted_sims[:10]
	'''

def q1_3():
	G = snap.TNGraph.Load(snap.TFIn("hw2-q1.graph"))

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

def cluster_and_PCA():
	final_cluster_dict = None
	with open('recursive_features_graph2.pkl', 'rb') as handle:
		final_cluster_dict = pickle.load(handle)

    # Now do kmeans first on the featuers, then show pca color coded
	print 'Kmeans'
	clusters = []
	for item in final_cluster_dict.itervalues():
		clusters.append(item)

	kmeans = KMeans(n_clusters=8, random_state=0).fit(clusters)
	centers = kmeans.cluster_centers_
	assigned_clusters = kmeans.predict(clusters)

	print 'PCA'
	pca = PCA(n_components=2)
	pca.fit(clusters)
	results = pca.transform(clusters)
	plt.scatter(results[:,0], results[:,1], c=assigned_clusters)
	plt.xlabel('First Principal Component')
	plt.ylabel('Second Principal Component')
	plt.title('RolX Algorithm Principal Components - Clustering on Feature Vectors')
	plt.show()

	# Now kmeans on PCA results
	kmeans = KMeans(n_clusters=8, random_state=0).fit(results)
	centers = kmeans.cluster_centers_
	assigned_clusters = kmeans.predict(results)

	# Plot again
	plt.scatter(results[:,0], results[:,1], c=assigned_clusters)
	plt.xlabel('First Principal Component')
	plt.ylabel('Second Principal Component')
	plt.title('RolX Algorithm Principal Components - Clustering on PCA')
	plt.show()

run_recursive_feats()
cluster_and_PCA()



