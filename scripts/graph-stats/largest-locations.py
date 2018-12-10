#!/usr/bin/env python3
import click

import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

from data import users
from collections import Counter

if __name__ == "__main__":
    locations = Counter(user['location'] for user in users() if user['location'] != None)

    for i, (location, size) in enumerate(locations.most_common(100)):
        print(i + 1, "&", location, "&", size, "\\\\")
