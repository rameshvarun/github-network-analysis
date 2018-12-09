#!/usr/bin/env python3
import click
import sys

import matplotlib.pyplot as plt

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

@cached('results/user-to-company.pickle')
def get_user_to_company():
    print("Generating user to company mapping...")
    return { user['id']: user['company'] for user in users() if user['company'] != None }

@cached('results/user-to-location.pickle')
def get_user_to_location():
    print("Generating user to location mapping...")
    return { user['id']: user['location'] for user in users() if user['location'] != None }

if __name__ == "__main__":
    user_to_orgs = get_user_to_orgs()
    user_to_company = get_user_to_company()
    user_to_location = get_user_to_location()

    communities = [c for c in load_communities("results/communities.txt") if len(c) >= COMMUNITY_MIN_SIZE]
    print("Number of communities:", len(communities))

    org_homogeneities = []
    company_homogeneities = []
    location_homogeneities = []

    with click.progressbar(communities) as bar:
        for community in bar:
            company_count = Counter(user_to_company[user] for user in community if user in user_to_company)
            location_count = Counter(user_to_location[user] for user in community if user in user_to_location)

            org_count = Counter()
            for user in community:
                org_count.update(user_to_orgs[user])

            most_common_org = org_count.most_common(1)
            if len(most_common_org) > 0:
                org_homogeneity = most_common_org[0][1] / len(community)
                org_homogeneities.append(org_homogeneity)

            most_common_company = company_count.most_common(1)
            if len(most_common_company) > 0:
                company_homogeneity = most_common_company[0][1] / len(community)
                company_homogeneities.append(company_homogeneity)

            most_common_location = location_count.most_common(1)
            if len(most_common_location) > 0:
                location_homogeneity = most_common_location[0][1] / len(community)
                location_homogeneities.append(location_homogeneity)

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True)
    fig.suptitle("Community Homogeneity")

    ax1.hist(org_homogeneities, log=True)
    ax1.set_xlabel('Org. Homogeneity')
    ax1.set_ylabel('Frequency')

    ax2.hist(company_homogeneities, log=True)
    ax2.set_xlabel('Company Homogeneity')
    ax2.set_ylabel('Frequency')

    ax3.hist(location_homogeneities, log=True)
    ax3.set_xlabel('Location Homogeneity')
    ax3.set_ylabel('Frequency')

    plt.show()
