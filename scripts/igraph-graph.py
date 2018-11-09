import click

from igraph import *
from data import followers, users

@click.command()
@click.argument('output', type=click.Path())
def generate_graph(output):
    graph = Graph(directed=True)

    print ("Reading data...")
    vertices = set()
    edges = set()
    for follow in followers():
        src, dst = follow['user_id'], follow['follower_id']
        vertices.add(src)
        vertices.add(dst)
        edges.add((src, dst))

    print ("Building graph edges...")
    graph.add_vertices(str(v) for v in vertices)
    graph.add_edges((str(a), str(b)) for a, b in edges)

    graph.write_pickle(output)

if __name__ == '__main__':
    generate_graph()
