from peewee import *

db = SqliteDatabase('agregat.db')

class Person(Model):
    user_id = CharField(null=True)
    user_name = CharField(null=True)
    user_link = CharField(null=True)
    group_id = CharField(null=True)
    group_name = CharField(null=True)
    group_link = CharField(null=True)
    message_text = TextField(null=True)
    media_files = TextField(null=True)

    class Meta:
        database = db # This model uses the "agregat.db" database.

Person.create_table()

