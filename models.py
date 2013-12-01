from peewee import *

db = SqliteDatabase('shrtnr.db', threadlocals=True)

class Url(Model):
    url = CharField()
    url_hash = CharField(unique=True)
    hits = IntegerField(default=0)
    key = CharField(null=True)

    enabled = BooleanField(default=True)
    created = DateTimeField()

    class Meta:
        database = db