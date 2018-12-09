#!/usr/bin/env python3
import click

import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

from utils import get_org_id_to_login, jaccard_similarity
from data import organization_members
from collections import defaultdict
from itertools import combinations

MINIMUM_ORG_SIZE = 20

if __name__ == "__main__":
    id_to_login = get_org_id_to_login()

    organizations = defaultdict(set)
    for record in organization_members():
        organizations[record['org_id']].add(record['user_id'])

    for org_id in list(organizations.keys()):
        if len(organizations[org_id]) < MINIMUM_ORG_SIZE:
            del organizations[org_id]

    print("Number of organizations:", len(organizations))

    org_similarities = [(jaccard_similarity(a_members, b_members), a, b) for (a, a_members), (b, b_members) in combinations(organizations.items(), 2)]
    org_similarities.sort(reverse=True)

    for i, (org_sim, org_a, org_b) in enumerate(org_similarities[:100]):
        name_a = id_to_login[org_a] if org_a in id_to_login else f"<UNKNOWN:{org_id}>"
        name_b = id_to_login[org_b] if org_b in id_to_login else f"<UNKNOWN:{org_id}>"
        print(i + 1, "&", name_a, "&", name_b, "&", org_sim, "\\\\")
