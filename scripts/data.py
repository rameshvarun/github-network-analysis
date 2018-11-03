from fastavro import reader

def followers():
    with open('data/followers.avro', 'rb') as file:
        for record in reader(file):
            yield record

def users():
    for userfile in ['data/users-0.avro', 'data/users-1.avro', 'data/users-2.avro']:
        with open(userfile, 'rb') as file:
            for record in reader(file):
                yield record
