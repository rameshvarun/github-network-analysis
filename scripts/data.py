from fastavro import reader
from utils import count_iterator


def followers():
    with open("data/followers.avro", "rb") as file:
        for record in reader(file):
            yield record


def users():
    for userfile in ["data/users-0.avro", "data/users-1.avro", "data/users-2.avro"]:
        with open(userfile, "rb") as file:
            for record in reader(file):
                yield record

def organization_members():
    for orgfile in ["data/organization_members.avro"]:
        with open(orgfile, "rb") as file:
            for record in reader(file):
                yield record

def watchers():
    for watcherfile in [
        "data/watchers-000000000000.avro",
        "data/watchers-000000000001.avro",
        "data/watchers-000000000002.avro",
        "data/watchers-000000000003.avro",
        "data/watchers-000000000004.avro",
        "data/watchers-000000000005.avro",
        "data/watchers-000000000006.avro",
        "data/watchers-000000000007.avro",
        "data/watchers-000000000008.avro",
        "data/watchers-000000000009.avro",
        "data/watchers-000000000010.avro",
    ]:
        with open(watcherfile, "rb") as file:
            for record in reader(file):
                yield record


if __name__ == "__main__":
    print("Counting users...")
    print("Number of users:", count_iterator(users()))

    print("Counting follows...")
    print("Number of follows:", count_iterator(followers()))

    print("Counting watchers...")
    print("Number of watchers:", count_iterator(watchers()))

    print("Couting orgs...")
    print("Number of organization members:", count_iterator(organization_members()))
