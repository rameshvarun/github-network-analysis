import snap
from data import followers, users

if __name__ == "__main__":
    graph = snap.TNGraph.New()

    print ("Adding users...")
    for user in users():
        graph.AddNode(user['id'])
    
    print ("Adding follow edges...")
    for follow in followers():
        graph.AddEdge(follow['user_id'], follow['follower_id'])

    FOut = snap.TFOut("results/snap-follow.graph")
    graph.Save(FOut)
    FOut.Flush()
