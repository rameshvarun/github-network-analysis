#!/usr/bin/env python3

import click
import sys

import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

from utils import load_communities, cached, jaccard_similarity, get_user_id_to_login
from data import organization_members, users
from collections import defaultdict

COMMUNITY_MIN_SIZE = 5

@cached('results/companies.pickle')
def get_companies():
    print("Generating companies...")
    companies = defaultdict(set)
    for user in users():
        if user['company'] != None:
            companies[user['company'].lower()].add(user['id'])

    return companies

if __name__ == "__main__":
    companies = get_companies()

    for company in list(companies.keys()):
        if len(companies[company]) < COMMUNITY_MIN_SIZE:
            del companies[company]

    print("Number of companies:", len(companies))

    communities = [c for c in load_communities("results/communities.txt") if len(c) >= COMMUNITY_MIN_SIZE]
    print("Number of communities:", len(communities))

    results = []
    with click.progressbar(companies.items()) as bar:
        for company, members in bar:
            best_match = max(jaccard_similarity(members, community) for community in communities)
            results.append((best_match, company, len(members)))

    results.sort(reverse=True)
    for i, (best_match, company, company_size) in enumerate(results[:100]):
        print(i + 1, "&", company, "&", company_size, "&", "{:.2f}".format(best_match), "\\\\")
