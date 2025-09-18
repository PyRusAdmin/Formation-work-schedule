from peewee import SqliteDatabase, Model, CharField, DateField

# Инициализация базы данных
db = SqliteDatabase('vacations.db')


class BaseModel(Model):
    class Meta:
        database = db


class Employee(BaseModel):
    name = CharField()  # Имя сотрудника
    vacation_start = DateField()  # Дата начала отпуска
    vacation_end = DateField()  # Дата окончания отпуска
    weekends = CharField()  # Храним выходные дни как строку JSON


# Функция для подключения к БД
def initialize_db():
    db.connect()
    db.create_tables([Employee])
