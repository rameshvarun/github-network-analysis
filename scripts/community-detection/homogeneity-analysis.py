#!/usr/bin/env python3
import click
import sys

import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

from utils import load_communities, cached, get_org_id_to_login
from data import organization_members, users

from collections import defaultdict, Counter

COMMUNITY_MIN_SIZE = 5

@cached('results/user-to-orgs.pickle')
def get_user_to_orgs():
    print("Generating user to orgs mapping...")
    user_to_orgs = defaultdict(set)
    for record in organization_members():
        user_to_orgs[record['user_id']].add(record['org_id'])
    return user_to_orgs

if __name__ == "__main__":
    user_to_orgs = get_user_to_orgs()
    # org_id_to_login = get_org_id_to_login()

    communities = [c for c in load_communities("results/communities.txt") if len(c) >= COMMUNITY_MIN_SIZE]
    print("Number of communities:", len(communities))

    with click.progressbar(communities) as bar:
        for community in bar:
            org_count = Counter()
            for user in community:
                org_count.update(user_to_orgs[user])
            org_homogeneity = org_count.most_common(1)[0][1] / len(community)
            print(org_homogeneity)
