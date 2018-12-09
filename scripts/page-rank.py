#!/usr/bin/env python2
import snap
import click

from data import users
from utils import get_user_id_to_login

@click.command()
@click.argument('input', type=click.Path())
def page_rank(input):
    id_to_login = get_user_id_to_login()

    print("Loading graph...")
    FIn = snap.TFIn(input)
    graph = snap.TNGraph.Load(FIn)

    print("Calculating page rank...")
    PRankH = snap.TIntFltH()
    snap.GetPageRank(graph, PRankH)

    scores = sorted([(PRankH[item], item) for item in PRankH], reverse=True)[:100]
    print([(id_to_login[id], score) for score, id in scores])

if __name__ == "__main__":
    page_rank()
