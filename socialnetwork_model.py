from peewee import SqliteDatabase, Model, CharField, ForeignKeyField, IntegrityError
from playhouse.dataset import DataSet
from loguru import logger

db = SqliteDatabase('social_network.db', pragmas={'foreign_keys': 1})


class BaseModel(Model):
    class Meta:
        database = db

class UserTable(BaseModel):
    user_id = CharField(primary_key=True, max_length=30)
    first_name = CharField(max_length=30)
    last_name = CharField(max_length=100)
    email = CharField()

class StatusTable(BaseModel):
    status_id = CharField(primary_key=True)
    user_id = ForeignKeyField(UserTable, on_delete='CASCADE')
    status_text = CharField()

class PictureTable(BaseModel):
    picture_id = CharField(primary_key=True)
    user_id = ForeignKeyField(UserTable, on_delete='CASCADE')
    tags = CharField(max_length=100)


db.connect()
db.create_tables([UserTable, StatusTable, PictureTable])
db.close()

ds = DataSet(db)
Users = ds["usertable"]
Statuses = ds["statustable"]
Pictures = ds["picturetable"]
# Users.insert(user_id='index_creation')
# Statuses.insert(status_id='index_creation')
# Users.create_index(["user_id"], unique=True)
# Statuses.create_index(["status_id"], unique=True)
# Users.delete(user_id='index_creation')
# Statuses.delete(status_id='index_creation')


def insert_table(database):

    def insert(**kwargs):
        try:
            database.insert(**kwargs)
            logger.info(f"Successfully inserted {kwargs}")
            return True
        except IntegrityError:
            logger.error(f"IntegrityError found when inserting {kwargs}")
            return False

    return insert


def search_table(database):

    def search(**kwargs):
        return database.find_one(**kwargs)

    return search


def update_table(database):

    def update(update_key, **kwargs):
        return database.update(columns=update_key,**kwargs)

    return update

def delete_table(database):

    def delete(**kwargs):
        return database.delete(**kwargs)

    return delete

def search_table_for_many(database):

    def search_many(**kwargs):
        return database.find(**kwargs)

    return search_many