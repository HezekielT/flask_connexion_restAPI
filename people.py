from flask import make_response, abort
from config import db
from models import (
    Person,
    PersonSchema,
)

def read_all():
    
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


def update(person_id, person):
    update_person = Person.query.filter(
        Person.person_id == person_id
    ).one_or_none()

    fname = person.get("fname")
    lname = person.get("lname")

    existing_person = (
        Person.query.filter(Person.fname == fname)
        .filter(Person.lname == lname)
        .one_or_none()
    )

    if update_person is None:
        abort(
            404, "Person not found for Id: {person_id}".format(person_id=person_id),
        )
    elif (existing_person is not None and existing_person.person_id != person_id):
        abort(409, "Person {fname}{lname} exists already".format(fname=fname,lname=lname),
    )
    else:

        schema = PersonSchema()
        update = schema.load(person, session=db.session)

        update.person_id = update_person.person_id
        db.session.merge(update)
        db.session.commit()

        data = schema.dump(update_person)

        return data, 200

def delete(person_id):
    person = Person.query.filter(Person.person_id == person_id).one_or_none()

    if person is not None:
        db.session.delete(person)
        db.session.commit()
        return make_response(
            "Person {person_id} deleted".format(person_id=person_id), 200
        )

    else:
        abort(
            404,
            "Person not found for Id: {person_id}".format(person_id=person_id),
        )