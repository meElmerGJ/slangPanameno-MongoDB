from mongoengine import Document, StringField, IntField


class Slangs(Document):
    word = StringField(required=True, max_length=50)
    meaning = StringField(required=True, max_length=200)
    words_generated = False




