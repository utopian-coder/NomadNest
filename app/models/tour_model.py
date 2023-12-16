from mongoengine import Document, StringField, FloatField, IntField

class Tour(Document):
    name = StringField(required=True)
    description = StringField()
    duration = IntField()
    price = FloatField()
    difficulty = StringField()
    ratings_quantity = IntField()
    ratings_average = FloatField()