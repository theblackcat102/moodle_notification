from peewee import (
    CharField,
    DateTimeField,
    TextField,
    ForeignKeyField,
    ManyToManyField,
    DeferredThroughModel,
    IntegerField,
    BooleanField,
    Model
)
import datetime
from playhouse.sqlite_ext import (JSONField, TextField, SqliteExtDatabase)
from datetime import datetime, timezone, timedelta

sqlite_db = SqliteExtDatabase('moodle.db',
    pragmas={'foreign_keys': 1,
        'journal_mode': 'wal',
        'cache_size': -1024*64})


class Notification(Model):
    
    # this should be a unique notify name
    # course-module name-notify rule
    # for example: deeplearning-assignmentlab01-notify new assignment

    name = TextField(unique=True)
    sendtime = DateTimeField(default=datetime.now, unique=True)

    class Meta:
        db_table = 'notification'
        database = sqlite_db

from telegram import send_msg

def send_notification(msg, parse_mode=None):
    '''
    msg: Must contain id and content attributes
    parse_mode: Telegram parse mode
    '''
    msg_id = msg['id']
    if not Notification.select().where(Notification.name == msg_id).exists():
        results = send_msg(msg['content'], parse_mode=parse_mode)
        if results['ok']:
            n = Notification.create(
                name=msg_id
            )
            n.save()
            return True
    return False


if __name__ == '__main__':
    sqlite_db.create_tables([Notification])
    # create_tables()
