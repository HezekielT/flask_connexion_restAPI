import os
from config import db
from models import Person

PEOPLE = [
    {
        "fname": "Doug",
        "lname": "Farrell",
        "notes": [
            ("Cool, a mini-blogging application!", "2019-01-06 22:17:54"),
            ("This could be useful", "2019-01-08 22:17:54"),
            ("Well, sort of useful", "2019-03-06 22:17:54"),
        ],
    },
    {
        "fname": "Kent",
        "lname": "Brockman",
        "notes": [
            (
                "I'm going to make really profound observations",
                "2019-01-07 22:17:54",
            ),
            (
                "Maybe they'll be more obvious than I thought",
                "2019-02-06 22:17:54",
            ),
        ],
    },
    {
        "fname": "Bunny",
        "lname": "Easter",
        "notes": [
            ("Has anyone seen my Easter eggs?", "2019-01-07 22:47:54"),
            ("I'm really late delivering these!", "2019-04-06 22:17:54"),
        ],
    },
]


if os.path.exists('people.db'):
    os.remove('people.db')

db.create_all()

for person in PEOPLE:
    p = Person(lname=person['lname'], fname=person['fname'])
    db.session.add(p)

db.session.commit()