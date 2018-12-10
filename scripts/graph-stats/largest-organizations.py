#!/usr/bin/env python3
import click

import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

from utils import get_org_id_to_login
from data import organization_members
from collections import defaultdict

if __name__ == "__main__":
    id_to_login = get_org_id_to_login()

    organizations = defaultdict(set)
    for record in organization_members():
        organizations[record['org_id']].add(record['user_id'])

    print("Number of organizations:", len(organizations))
    largest_orgs = sorted([(len(members), org_id) for org_id, members in organizations.items()], reverse=True)[:100]
    for i, (org_size, org_id) in enumerate(largest_orgs):
        org_name = id_to_login[org_id] if org_id in id_to_login else f"<UNKNOWN:{org_id}>"
        print(i + 1, "&", org_name, "&", org_size, "\\\\")
