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

class User(BaseModel):
    user_id: int = IntegerField(primary_key=True)
    username: str = CharField()
    first_name: str  = CharField()
    last_name: str = CharField(null=True)
    total_debt: int = IntegerField(default=0)

class Debt(BaseModel):
    debt_id: int = AutoField(primary_key=True)
    user = ForeignKeyField(User, backref='debts')
    date_start: date = DateField(default=date.today)
    date_end: date = DateField()
    is_done: bool = BooleanField(default=False)
    product: str = CharField()
    total_price: float = FloatField()
    pay_off_price: float = FloatField()

def create_models():
    db.create_tables(BaseModel.__subclasses__())