import re
from peewee import *

db = SqliteDatabase(r'tgbot\models\agregat3.db')

class Product(Model):
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


# Connect to a Postgres database.
pg_db = PostgresqlDatabase('keywords', user='postgres', password='123456',
                           host='192.168.56.6', port=5432)


class BaseModel(Model):
    """A base model that will use our Postgresql database"""
    class Meta:
        database = pg_db

class Keywords(BaseModel):
    keyword = TextField()
    category = TextField()



# a = """✅ Telefon sotiladi 
# 📱 Nomi: Redmi 9C
# 🛠 Xolati: tiniq hamayogi radnoy
# 🗃 Xotira: 4/64Gb
# 🔋 Batareya 5000 MhA
# 📦 Karobka dakumenti: yoq
# 💰 Narxi: 850.000 ozro kami bor
# 🔄 Obmen yoq sorameng
# 🏠 Andijon shaxar
# """

# query = Keywords.select()

# for quer in query:
#     quer: Keywords

#     # if  f"{str(quer.keyword).lower()}" in a.lower():
#     #     print(quer.category)
#     #     print(quer.keyword)
#     # else:
#     #     continue

#     if re.match(f'.?{str(quer.keyword).lower()}', a.lower(), re.DOTALL):
#         print(quer.category)
#         print(quer.keyword)