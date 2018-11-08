import snap
import click

from data import followers, users

@click.command()
@click.option('--prune', is_flag=True)
@click.argument('output', type=click.Path())
def generate_graph(prune, output):
    graph = snap.TNGraph.New()

    # If we aren't pruning edges, then we need the whole graph.
    if not prune:
        print ("Adding users...")
        for user in users():
            graph.AddNode(user['id'])

    print ("Adding follow edges...")
    for follow in followers():
        # If source or destination don't exist, then we need to create them.
        src, dst = follow['user_id'], follow['follower_id']
        if not graph.IsNode(src):
            graph.AddNode(src)
        if not graph.IsNode(dst):
            graph.AddNode(dst)

        graph.AddEdge(src, dst)

    print("Nodes:", graph.GetNodes())
    print("Edges:", graph.GetEdges())

    FOut = snap.TFOut(output)
    graph.Save(FOut)
    FOut.Flush()


if __name__ == '__main__':
    generate_graph()
