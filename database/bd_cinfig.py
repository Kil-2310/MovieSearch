from datetime import date
from peewee import (
    AutoField,
    BooleanField,
    CharField,
    DateField,
    ForeignKeyField,
    IntegerField,
    Model,
    SqliteDatabase,
    FloatField
)

from config_data.config import DB_PATH

db = SqliteDatabase(DB_PATH, check_same_thread=False)

class BaseModel(Model):
    class Meta:
        database = db

def create_models():
    db.create_tables(BaseModel.__subclasses__())