"""Mapping between topics and people who are knowledgeable about them."""

from dataclasses import dataclass
import os

from autokitteh.google import google_sheets_client


DIRECTORY_GOOGLE_SHEET_ID = os.getenv("DIRECTORY_GOOGLE_SHEET_ID", "")

gsheets = google_sheets_client("mygsheets").spreadsheets().values()


@dataclass
class Person:
    """A person in the directory."""

    name: str
    slack_id: str
    topics: list[str]


def load() -> dict[str, list[Person]]:  # topic -> list of people
    vs = (
        gsheets.get(spreadsheetId=DIRECTORY_GOOGLE_SHEET_ID, range="A1:C100")
        .execute()
        .get("values", [])
    )

    ppl = [Person(v[0], v[1], v[2].split(",")) for v in vs]

    topics = {topic for person in ppl for topic in person.topics}

    return {
        topic: [person for person in ppl if topic in person.topics] for topic in topics
    }
