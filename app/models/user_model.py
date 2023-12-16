from mongoengine import Document, StringField

class User(Document):
    name: StringField()
    email: StringField()
    password: StringField()