"""Docstring for pydantic.dnd.data"""

import random


# TODO: Make the AI come up with these.

_CLASS_NAMES = [
    "Warrior",
    "Mage",
    "Rogue",
    "Cleric",
]

_RACE_NAMES = [
    "Human",
    "Elf",
    "Dwarf",
    "Halfling",
    "Half-Elf",
    "Half-Orc",
    "Dragonborn",
    "Gnome",
    "Tiefling",
]

_NAMES = {
    "Human": [
        "Aldric",
        "Gareth",
        "Theron",
        "Cedric",
        "Rowan",
        "Elara",
        "Seraphina",
        "Lyra",
        "Brynn",
        "Aria",
    ],
    "Elf": [
        "Thalion",
        "Aerendil",
        "Legolas",
        "Finrod",
        "Galaeron",
        "Arwen",
        "Silvariel",
        "Naeris",
        "Lúthien",
        "Amriel",
    ],
    "Dwarf": [
        "Thorin",
        "Gimli",
        "Bruenor",
        "Balin",
        "Dwalin",
        "Mera",
        "Kathra",
        "Finellen",
        "Bardryn",
        "Gurdis",
    ],
    "Halfling": [
        "Bilbo",
        "Merric",
        "Roscoe",
        "Osborn",
        "Lyle",
        "Lidda",
        "Vani",
        "Cora",
        "Trym",
        "Shaena",
    ],
    "Half-Elf": [
        "Kael",
        "Finnian",
        "Talin",
        "Celeste",
        "Mira",
        "Quinn",
        "Elian",
        "Seren",
        "Aiden",
        "Rhys",
    ],
    "Half-Orc": [
        "Grog",
        "Thrak",
        "Krusk",
        "Uruk",
        "Gorak",
        "Shava",
        "Keth",
        "Yevelda",
        "Baggi",
        "Vola",
    ],
    "Dragonborn": [
        "Drax",
        "Balasar",
        "Torinn",
        "Rhogar",
        "Arjhan",
        "Kava",
        "Nala",
        "Thava",
        "Mishann",
        "Sora",
    ],
    "Gnome": [
        "Dimble",
        "Fonkin",
        "Glim",
        "Jebeddo",
        "Sindri",
        "Bree",
        "Caramip",
        "Nissa",
        "Oda",
        "Waywocket",
    ],
    "Tiefling": [
        "Zephyr",
        "Akira",
        "Damakos",
        "Kallista",
        "Nemeia",
        "Hope",
        "Glory",
        "Torment",
        "Mercy",
        "Sorrow",
    ],
}


def random_character_attrs() -> tuple[str, str, str]:
    """Return random character attributes

    Returns a tuple of (class, race, name).
    """
    cls = random.choice(_CLASS_NAMES)
    race = random.choice(_RACE_NAMES)
    name = random.choice(_NAMES[race])
    return cls, race, name
