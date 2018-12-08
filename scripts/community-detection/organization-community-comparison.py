#!/usr/bin/env python3
import click

from utils import load_communities, cached, jaccard_similarity, get_org_id_to_login
from data import organization_members, users
from collections import defaultdict

COMMUNITY_MIN_SIZE = 5

if __name__ == "__main__":
    id_to_login = get_org_id_to_login()

    communities = [c for c in load_communities("results/communities.txt") if len(c) >= COMMUNITY_MIN_SIZE]
    print("Number of communities:", len(communities))

    organizations = defaultdict(set)
    for record in organization_members():
        organizations[record['org_id']].add(record['user_id'])

    for org_id in list(organizations.keys()):
        if len(organizations[org_id]) < COMMUNITY_MIN_SIZE:
            del organizations[org_id]

    print("Number of organizations:", len(organizations))

    results = []
    with click.progressbar(organizations.items()) as bar:
        for org_id, org_members in bar:
            best_match = max(jaccard_similarity(org_members, community) for community in communities)
            results.append((best_match, org_id, len(org_members)))

    results.sort(reverse=True)
    for i, (best_match, org_id, org_size) in enumerate(results[:100]):
        org_name = id_to_login[org_id] if org_id in id_to_login else f"<UNKNOWN:{org_id}>"
        print(i + 1, "&", org_name, "&", org_size, "&", "{:.2f}".format(best_match), "\\\\")
