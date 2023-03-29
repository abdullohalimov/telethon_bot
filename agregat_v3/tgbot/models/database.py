from peewee import *

db = SqliteDatabase(r'tgbot\models\agregat3.db')

class Person(Model):
    user_id = CharField(null=True)
    user_name = CharField(null=True)
    user_link = CharField(null=True)
    group_id = CharField(null=True)
    group_name = CharField(null=True)
    group_link = CharField(null=True)
    message_id = TextField(null=True)
    message_text = TextField(null=True)
    category = TextField(null=True)
    media_files = TextField(null=True)
    datatime = TextField(null=True)
    status = TextField(null=True)

    class Meta:
        database = db # This model uses the "agregat.db" database.

Person.create_table(Person)

