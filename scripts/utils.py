import ast
import pickle
import os


def count_iterator(it):
    """
    Count the number of elements in an iterator.
    """
    count = 0
    for val in it:
        count += 1
    return count


def load_communities(communities_file):
    communities = []
    with open(communities_file, "r") as file:
        for line in file:
            communities.append(set(ast.literal_eval(line)))
    return communities


def cached(cachefile):
    """
    A function that creates a decorator which will use "cachefile" for caching
    the results of the decorated function "fn".
    """

    protocol = pickle.HIGHEST_PROTOCOL
    cachefile = cachefile  + '.' + str(protocol)

    def decorator(fn):  # define a decorator for a function "fn"
        def wrapped(
            *args, **kwargs
        ):  # define a wrapper that will finally call "fn" with all arguments
            # if cache exists -> load it and return its content
            if os.path.exists(cachefile):
                with open(cachefile, "rb") as cachehandle:
                    return pickle.load(cachehandle)

            # execute the function with all arguments passed
            res = fn(*args, **kwargs)

            # write to cache file
            with open(cachefile, "wb") as cachehandle:
                pickle.dump(res, cachehandle, protocol=protocol)

            return res

        return wrapped

    return decorator  # return this "customized" decorator that uses "cachefile"


def jaccard_similarity(a, b):
    """
    Calculates the Jaccard similarity of two sets.
    """
    return len(a & b) / len(a | b)

@cached('results/user_id_to_login_mapping.pickle')
def get_user_id_to_login():
    from data import users
    print ("Generating id->login mappings...")
    return { user['id']: user['login'] for user in users() }

@cached('results/org_id_to_login_mapping.pickle')
def get_org_id_to_login():
    from data import users
    print ("Generating id->login mappings...")
    return { user['id']: user['login'] for user in users() if user['type'] == 'ORG' }
