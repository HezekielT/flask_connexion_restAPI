from datetime import datetime
from config import db, ma
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields


class Person(db.Model):
    __tablename__ = "person"
    person_id = db.Column(db.Integer, primary_key=True)
    lname = db.Column(db.String(32))
    fname = db.Column(db.String(32))
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    notes = db.relationship(
        'Note',
        backref='person',
        cascade='all, delete, delete-orphan',
        single_parent=True,
        order_by='desc(Note.timestamp)'
    )

class Note(db.Model):
    __tablename__ = 'note'
    note_id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.person_id'))
    content = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class PersonSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Person
        include_relationships = True
        load_instance = True
    notes = fields.Nested('PersonNoteSchema', default=[], many=True)

class PersonNoteSchema(SQLAlchemyAutoSchema):
    note_id = fields.Int()
    person_id = fields.Int()
    content = fields.Str()
    timestamp = fields.Str()

class NoteSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Note
        include_relationships = True
        load_instance = True
    person = fields.Nested('NotePersonSchema', default=None)

class NotePersonSchema(SQLAlchemyAutoSchema):
    person_id = fields.Int()
    lname = fields.Str()
    fname = fields.Str()
    timestamp = fields.Str()