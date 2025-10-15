# -*- coding: utf-8 -*-
import json
from datetime import datetime

from peewee import SqliteDatabase, Model, CharField, TextField, DateTimeField
from loguru import logger

"""Запись данных из таблицы ReportCard10 в ReportCard12"""

# Инициализация базы данных
db = SqliteDatabase('vacations.db')


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


# def copy_data():
employees = []
for emp in ReportCard10.select():
    employees.append({
        "КСП": emp.ksp,
        "Наименование": emp.name,
        "Категория": emp.category,
        "Профессия": emp.profession,
        "Статус": emp.status,
        "Сокращение": emp.abbreviation,
        "Разряд": emp.grade,
        "Таб": emp.tab,
        "ФИО": emp.fio,
        "Тариф": emp.salary,
        "days": json.loads(emp.days)
    })

for data in employees:
    logger.info(data)

for row in employees:
    ReportCard12.create(
        ksp=row["КСП"],
        name=row["Наименование"],
        category=row["Категория"],
        profession=row["Профессия"],
        status=row["Статус"],
        abbreviation=row.get("Сокращение", ""),
        grade=row.get("Разряд", ""),
        tab=row["Таб"],
        fio=row["ФИО"],
        salary=row["Тариф"],
        days=json.dumps(row["days"], ensure_ascii=False)
    )
