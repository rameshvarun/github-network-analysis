import snap
from data import followers, users

if __name__ == "__main__":
    graph = snap.TNGraph.New()

    print ("Adding users...")
    for user in users():
        graph.AddNode(user['id'])

    print ("Adding follow edges...")
    for follow in followers():
        src, dst = follow['user_id'], follow['follower_id']
        if not graph.IsNode(src):
            print("Adding missing node:", src)
            graph.AddNode(src)

        if not graph.IsNode(dst):
            print("Adding missing node:", dst)
            graph.AddNode(dst)
            
        graph.AddEdge(src, dst)

    FOut = snap.TFOut("results/snap-follow.graph")
    graph.Save(FOut)
    FOut.Flush()
