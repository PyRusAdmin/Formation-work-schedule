from datetime import datetime

from peewee import SqliteDatabase, Model, CharField, DateField, TextField, DateTimeField

from utilities.work_with_excel import get_data_from_excel

# Инициализация базы данных
db = SqliteDatabase('data/vacations.db')


class BaseModel(Model):
    class Meta:
        database = db


class ReportCard10(BaseModel):
    """График выходов сотрудников на октябрь 2025"""
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


class ReportCard11(BaseModel):
    """График выходов сотрудников на ноябрь 2025"""
    ksp = CharField()  # Код подразделения
    name = CharField()  # Наименование подразделения
    category = CharField()  # Категория
    profession = CharField()  # Должность
    status = CharField()  # Статус
    abbreviation = CharField(null=True)  # Аббревиатура
    grade = CharField(null=True)  # Класс
    tab = CharField()  # Табельный номер
    fio = CharField()  # ФИО
    salary = CharField()  # Зарплата
    days = TextField()  # Храним JSON как текст
    date_change = DateTimeField(default=datetime.now)  # Дата изменения графика 🆕 Новая колонка


class ReportCard12(BaseModel):
    """График выходов сотрудников на декабрь 2025"""
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


def initialize_db():
    """Инициализация БД и создание таблиц"""

    db.connect()

    # Проверяем, есть ли колонка admission_date в таблице datastaff
    columns = [col.name for col in db.get_columns('datastaff')]
    if 'admission_date' not in columns:
        db.execute_sql("ALTER TABLE datastaff ADD COLUMN admission_date DATE;")
    # if 'status' not in columns:
    #     db.execute_sql("ALTER TABLE datastaff ADD COLUMN status;")
    # if 'salary' not in columns:
    #     db.execute_sql("ALTER TABLE datastaff ADD COLUMN salary;")

    db.create_tables([Employee])
    db.create_tables([ReportCard10])  # График выходов сотрудников на октябрь 2025
    db.create_tables([ReportCard11])  # График выходов сотрудников на ноябрь 2025
    db.create_tables([ReportCard12])  # График выходов сотрудников на декабрь 2025

    db.create_tables([DataStaff])


class DataStaff(BaseModel):
    """Данные о сотрудниках"""
    service_number = CharField(unique=True)  # Табельный номер
    person = CharField()  # ФИО
    profession = CharField()  # Должность
    dismissal_date = DateField(null=True)  # 🆕 Дата увольнения

    admission_date = DateField(null=True)   # Дата приема

    ksp = CharField()  # Код подразделения
    status = CharField()  # Статус
    salary = CharField()  # Зарплата



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
