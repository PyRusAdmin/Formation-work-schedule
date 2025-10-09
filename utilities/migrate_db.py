# -*- coding: utf-8 -*-
from peewee import DateField
from playhouse.migrate import SqliteMigrator, migrate

# Импорт твоей базы из database.py
from database import db  # убедись, что объект базы называется db

migrator = SqliteMigrator(db)

# Добавляем новую колонку "date_change"
with db.atomic():
    migrate(
        migrator.add_column('reportcard', 'date_change', DateField(null=True))
    )

print("✅ Колонка 'date_change' успешно добавлена!")
