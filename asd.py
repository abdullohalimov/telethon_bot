from peewee import *

db = SqliteDatabase('agregat.db')

class Person(Model):
    user_id = CharField(null=True)
    group_id = CharField(null=True)
    message_text = TextField(null=True)
    media_files = BlobField(null=True)

    class Meta:
        database = db # This model uses the "people.db" database.

Person.create_table()

