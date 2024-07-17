# TODO: from collections import namedtuple

STAFF = [
    ("itay", "U03C3MTG76J", ["cats"]),
    ("daniel", "U05D59PKKFF", ["docs"]),
    ("efi", "U05HDSWAS82", ["pharmacuticals"]),
    ("haim", "U03D048HETA", ["russian"]),
]

TOPICS = set([t for person in STAFF for t in person[2]])


def find_by_topic(topic: str):
    return [person for person in STAFF if topic in person[2]]
