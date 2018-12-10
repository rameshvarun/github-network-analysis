import snap
import click
import sys

from data import watchers

@click.command()
@click.option('--prune', is_flag=True)
@click.argument('output', type=click.Path())
def generate_graph(prune, output):
    graph = snap.TUNGraph.New()

    print ("Adding watchers...")
    for watcher in watchers():
        
        # If source or destination don't exist, then we need to create them.
        src, dst = watcher['user_id'], watcher['repo_id']
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
