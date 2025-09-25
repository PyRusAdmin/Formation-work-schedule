from peewee import SqliteDatabase, Model, CharField, DateField

# Инициализация базы данных
db = SqliteDatabase('data/vacations.db')


class BaseModel(Model):
    class Meta:
        database = db


class Employee(BaseModel):
    name = CharField()  # Имя сотрудника
    vacation_start = DateField()  # Дата начала отпуска
    vacation_end = DateField()  # Дата окончания отпуска


# Функция для подключения к БД
def initialize_db():
    db.connect()
    db.create_tables([Employee])
    db.create_tables([DataStaff])


class DataStaff(BaseModel):
    """Данные о сотрудниках"""
    service_number = CharField()  # Табельный номер
    person = CharField()  # ФИО
    profession = CharField()  # Должность


def writing_employee_database():
    """Запись данных в БД данных о сотрудниках"""
    pass
