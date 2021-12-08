from flask import make_response, abort
from config import db
from models import (
    Person,
    PersonSchema,
)

def read_all():
    """
    This function responds to a request for /api/people
    with the complete lists of people
    :return:        json string of list of people
    """
    # Create the list of people from our data
    people = Person.query.order_by(Person.lname).all()
    person_schema = PersonSchema(many=True)  
    return person_schema.dump(people).data  

def read_one(person_id):
    person = Person.query \
        .filter(Person.person_id == person_id) \
            .one_or_none()
    if person is not None:
        person_schema = PersonSchema()
        return person_schema.dump(person).data
    else:
        abort(
            404, "Person not found for Id: {peerson_id}".format(person_id=person_id)
        )

    return person


def create(person):
    
    lname = person.get("lname", None)
    fname = person.get("fname", None)
    existing_person = Person.query \
        .filter(Person.fname == fname) \
            .filter(Person.lname == lname) \
                .one_or_none()
    if existing_person is None:
        schema = PersonSchema()
        new_person = schema.load(person, session=db.session).data

        db.session.add(new_person)
        db.session.commit()

        return schema.dump(new_person).data, 201
    # Otherwise, they exist, that's an error
    else:
        abort(
            409,
            f"Person {fname}{lname} already exists",
        )


def update(lname, person):
    """
    This function updates an existing person in the people structure
    :param lname:   last name of person to update in the people structure
    :param person:  person to update
    :return:        updated person structure
    """
    # Does the person exist in people?
    if lname in PEOPLE:
        PEOPLE[lname]["fname"] = person.get("fname")
        PEOPLE[lname]["timestamp"] = get_timestamp()

        return PEOPLE[lname]

    # otherwise, nope, that's an error
    else:
        abort(
            404, "Person with last name {lname} not found".format(lname=lname)
        )


def delete(lname):
    """
    This function deletes a person from the people structure
    :param lname:   last name of person to delete
    :return:        200 on successful delete, 404 if not found
    """
    # Does the person to delete exist?
    if lname in PEOPLE:
        del PEOPLE[lname]
        return make_response(
            "{lname} successfully deleted".format(lname=lname), 200
        )

    # Otherwise, nope, person to delete not found
    else:
        abort(
            404, "Person with last name {lname} not found".format(lname=lname)
        )