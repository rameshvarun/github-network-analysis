from data import followers, users
from collections import Counter
from itertools import islice

if __name__ == "__main__":
    print ("Generating id->login mappings...")
    id_to_login = { user['id']: user['login'] for user in users() }

    print ("Counting followers...")
    counter = Counter()
    counter.update(record['follower_id'] for record in followers())

    print ("Top 100 most followed users:")
    print ([(id_to_login[id], followers) for (id, followers) in counter.most_common(100)])
