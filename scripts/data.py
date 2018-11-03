from fastavro import reader
from utils import count_iterator

def followers():
    with open('data/followers.avro', 'rb') as file:
        for record in reader(file):
            yield record

def users():
    for userfile in ['data/users-0.avro', 'data/users-1.avro', 'data/users-2.avro']:
        with open(userfile, 'rb') as file:
            for record in reader(file):
                yield record

if __name__ == "__main__":
    print("Counting users...")
    print("Number of users:", count_iterator(users()))

    print("Counting follows...")
    print("Number of follows:", count_iterator(followers()))
