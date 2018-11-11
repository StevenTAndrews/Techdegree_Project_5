import datetime

from peewee import *



DATABASE = SqliteDatabase('journal.db')

class Entry(Model):
    timestamp = DateTimeField(default=datetime.datetime.now)
    title = CharField(unique=True)
    time_spent = IntegerField()
    content = TextField()
    resources = TextField()

    class Meta:
        database = DATABASE
        order_by = ('-timestamp',)


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Entry], safe=True)
    DATABASE.close()