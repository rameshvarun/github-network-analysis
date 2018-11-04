import snap
from data import users

if __name__ == "__main__":
    print ("Generating id->login mappings...")
    id_to_login = { user['id']: user['login'] for user in users() }

    print("Loading graph...")
    FIn = snap.TFIn("results/snap-follow.graph")
    graph = snap.TNGraph.Load(FIn)

    print("Calculating page rank...")
    PRankH = snap.TIntFltH()
    snap.GetPageRank(graph, PRankH)

    scores = sorted([(PRankH[item], item) for item in PRankH], reverse=True)[:100]
    print([(id_to_login[id], score) for score, id in scores])
