import snap
from data import users
from utils import cached, get_user_id_to_login

# @cached('results/login_to_id.pickle')
# def get_login_to_id():
#     print ("Generating login->id mappings...")
#     return { user['login']: user['id'] for user in users() }

if __name__ == "__main__":
    print("Loading graph...")
    FIn = snap.TFIn("results/snap-follow.graph")
    graph = snap.TNGraph.Load(FIn)
    
    nodes = set([959479])

    for i in range(2):
        NodeVec = snap.TIntV()
        snap.GetNodesAtHop(graph, 959479, i, NodeVec, False)
        for item in NodeVec:
            nodes.add(item)

    sg_nodes = snap.TIntV()
    for node in nodes:
        sg_nodes.Add(node)
    subgraph = snap.GetSubGraph(graph, sg_nodes)

    labels = snap.TIntStrH()
    for node in nodes:
        labels[node] = "UNKNOWN"

    for user in users():
        if user['id'] in nodes:
            labels[user['id']] = user['login']

    snap.DrawGViz(subgraph, snap.gvlDot, "graph.png", "githubpy Neighborhood", labels)

    # ni = graph.GetNI(58)
    # followers = [ni.GetInNId(i) for i in range(ni.GetInDeg())]
    # followees = [ni.GetOutNId(i) for i in range(ni.GetOutDeg())]
    # print(followers, followees)
