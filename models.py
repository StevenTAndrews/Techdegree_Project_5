import datetime

from peewee import *
from slugify import slugify



DATABASE = SqliteDatabase('journal.db')

class Entry(Model):
    timestamp = DateTimeField(default=datetime.datetime.now)
    title = CharField()
    slug = CharField(unique=True)
    time_spent = IntegerField()
    content = TextField()
    resources = TextField()

    class Meta:
        database = DATABASE


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Entry], safe=True)
    DATABASE.close()