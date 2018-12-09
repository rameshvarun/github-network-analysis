#!/usr/bin/env python3

import os
import sys
import click

from collections import Counter

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

from utils import load_communities, get_user_id_to_login, cached
from data import followers

@cached('results/follower-counts.pickle')
def get_follow_counts():
    print ("Generating follow counts...")
    counter = Counter()
    counter.update(record['follower_id'] for record in followers())
    return counter

@click.command()
@click.argument('input', type=click.Path())
def largest_community(input):
    user_id_to_login = get_user_id_to_login()

    communities = load_communities(input)
    print("Number of communities:", len(communities))

    largest_community = max(communities, key=lambda c: len(c))
    print("Largest community size:", len(largest_community))

    follow_counts = get_follow_counts()

    largest_community = list(largest_community)
    largest_community.sort(key=lambda id: follow_counts[id], reverse=True)
    print([(user_id_to_login[user] if user in user_id_to_login else f"UNKNOWN:{user}") for user in largest_community])

if __name__ == "__main__":
    largest_community()
