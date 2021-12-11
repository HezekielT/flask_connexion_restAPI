from sqlalchemy import schema
from models import NoteSchema, Person, Note
from flask import abort, make_response
from config import db

def read_all():
    notes = Note.query.order_by(db.desc(Note.timestamp)).all()
    note_schema = NoteSchema(many=True, exclude=["person.notes"])

    data = note_schema.dump(notes).data
    return data 

def read_one(person_id, note_id):
    """
    This function responds to a request for 
    /api/people/{person_id}/notes/{note_id}
    with one matching note for the associated person
    """
    note = (
        Note.query.join(Person, Person.person_id == Note.person_id)
        .filter(Person.person_id == person_id)
        .filter(Note.note_id == note_id)
        .one_or_none()
    )

    if note is not None:
        note_schema = NoteSchema()
        data = note_schema.dump(note).data
        return data

    else:
        abort(404, f"Note not found for Id: {note_id}")

def create(person_id, note):
    person = Person.query.filter(Person.person_id == person_id).one_or_none()

    if person is None:
        abort(404, f"Person not found for Id: {person_id}")
    note_schema = NoteSchema()
    new_note = note_schema.load(note, session = db.session)
    person.notes.append(new_note)
    db.session.commit()

    data = schema.dump(new_note)
    return data, 201

def update(person_id, note_id, note):
    existing_note = (
        Person.query.join(Person, Person.person_id == Note.person_id)
        .filter(Note.note_id == note_id)
        .one_or_none()
    )

    if existing_note is None:
        abort(404, f"No note found")

    note_schema = NoteSchema()
    update = schema.load(note, session=db.session)

    update.person_id = existing_note.person_id
    update.note_id = existing_note.note_id

    db.session.merge(update)
    db.session.commit()

    data = schema.dump(existing_note)
    return data, 200

def delete(person_id, note_id):
    note = (
        Note.query.filter(Person, Person.person_id == person_id)
        .filter(Note.note_id == note_id)
        .one_or_none()
    )

    if note is not None:
        db.session.delete(note)
        db.session.commit()
        return make_response(
            "Note {note_id} deleted".format(note_id=note_id), 200
        )
    else:
        abort(404, f"Note not found for ID: {note_id}")