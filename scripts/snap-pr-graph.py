import snap
import click
import sys

from data import pull_requests

@click.command()
@click.option('--prune', is_flag=True)
@click.argument('output', type=click.Path())
def generate_graph(prune, output):
    graph = snap.TNGraph.New()


    print ("Adding PRs...")
    for pr in pull_requests():
        # If source or destination don't exist, then we need to create them.
        src, dst = pr['pr_creator'], pr['repo_owner']

        # add this to fix outlier
        if src is None or dst is None:
            continue

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

    # Now go ahead and remove all the edges


if __name__ == '__main__':
    generate_graph()
