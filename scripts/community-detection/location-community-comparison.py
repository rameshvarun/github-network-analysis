#!/usr/bin/env python3
import click
import sys

import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

from utils import load_communities, cached, jaccard_similarity, get_user_id_to_login
from data import organization_members, users
from collections import defaultdict

COMMUNITY_MIN_SIZE = 5

@cached('results/locations.pickle')
def get_locations():
    print("Generating locations...")
    locations = defaultdict(set)
    for user in users():
        if user['location']:
            locations[user['location']].add(user['id'])
    return locations

if __name__ == "__main__":
    locations = get_locations()

    for location in list(locations.keys()):
        if len(locations[location]) < COMMUNITY_MIN_SIZE:
            del locations[location]

    print("Number of locations:", len(locations))

    communities = [c for c in load_communities("results/communities.txt") if len(c) >= COMMUNITY_MIN_SIZE]
    print("Number of communities:", len(communities))

    results = []
    with click.progressbar(locations.items()) as bar:
        for location, members in bar:
            best_match = max(jaccard_similarity(members, community) for community in communities)
            results.append((best_match, location, len(members)))

    results.sort(reverse=True)
    for i, (best_match, location, location_size) in enumerate(results[:100]):
        print(i + 1, "&", location, "&", location_size, "&", "{:.2f}".format(best_match), "\\\\")
