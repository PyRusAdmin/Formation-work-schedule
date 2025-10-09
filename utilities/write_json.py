# -*- coding: utf-8 -*-
# Загружаем JSON из файла
import json

from database import ReportCard

with open("../data/data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Сохраняем в базу
for row in data:
    ReportCard.create(
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

print("Данные успешно сохранены!")
