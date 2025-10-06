from datetime import datetime

from peewee import SqliteDatabase, Model, CharField, DateField, TextField, DateTimeField

from work_with_excel import get_data_from_excel

# Инициализация базы данных
db = SqliteDatabase('data/vacations.db')


class BaseModel(Model):
    class Meta:
        database = db


class ReportCard(BaseModel):
    """График выходов сотрудников"""
    ksp = CharField()
    name = CharField()
    category = CharField()
    profession = CharField()
    status = CharField()
    abbreviation = CharField(null=True)
    grade = CharField(null=True)
    tab = CharField()
    fio = CharField()
    salary = CharField()
    days = TextField()  # Храним JSON как текст
    date_change = DateTimeField(default=datetime.now)  # Дата изменения графика 🆕 Новая колонка


class Employee(BaseModel):
    service_number = CharField()  # Имя сотрудника
    vacation_start = DateField()  # Дата начала отпуска
    vacation_end = DateField()  # Дата окончания отпуска


# Функция для подключения к БД
def initialize_db():
    db.connect()
    db.create_tables([Employee])
    db.create_tables([ReportCard])
    db.create_tables([DataStaff])


class DataStaff(BaseModel):
    """Данные о сотрудниках"""
    service_number = CharField(unique=True)  # Табельный номер
    person = CharField()  # ФИО
    profession = CharField()  # Должность


def writing_employee_database():
    """Запись данных в БД данных о сотрудниках (без дубликатов)"""
    data_list = get_data_from_excel()

    with db.atomic():
        for data in data_list:
            DataStaff.get_or_create(
                service_number=data[5],
                defaults={
                    "person": data[6],
                    "profession": data[3]
                }
            )
