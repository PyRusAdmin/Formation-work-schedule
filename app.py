# -*- coding: utf-8 -*-
import json
from datetime import date, datetime
from pathlib import Path
from typing import List

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from loguru import logger
from pydantic import BaseModel

from database import initialize_db, ReportCard10

app = FastAPI()  # Создаем экземпляр FastAPI
# Монтируем статические файлы
app.mount('/static', StaticFiles(directory='static'), name='static')
# Создаем экземпляр Jinja2Templates
templates = Jinja2Templates(directory="templates")

# Инициализация БД при запуске приложения
initialize_db()


# Модели Pydantic
class EmployeeCreate(BaseModel):
    service_number: str
    vacation_start: date
    vacation_end: date


class EmployeeResponse(BaseModel):
    id: int
    service_number: str
    vacation_start: date
    vacation_end: date


DATA_FILE = Path("data/data.json")


@app.get("/data")
async def get_data():
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
    return employees


@app.post("/data")
async def save_data(request: Request):
    """Сохранение данных в БД и запись даты изменения"""
    new_data = await request.json()
    now = datetime.now()  # текущее время

    for row in new_data:
        emp, created = ReportCard10.get_or_create(tab=row["Таб"])
        emp.ksp = row["КСП"]
        emp.name = row["Наименование"]
        emp.category = row["Категория"]
        emp.profession = row["Профессия"]
        emp.status = row["Статус"]
        emp.abbreviation = row.get("Сокращение", "")
        emp.grade = row.get("Разряд", "")
        emp.fio = row["ФИО"]
        emp.salary = row["Тариф"]
        emp.days = json.dumps(row["days"], ensure_ascii=False)
        emp.date_change = now  # 🕒 записываем текущие дату и время
        emp.save()
    return {"status": "ok"}


@app.get("/report_card_10", response_model=None)
async def report_card_10(request: Request):
    """
    Страница формирования табеля сотрудников октябрь 2025 года
    """
    return templates.TemplateResponse("work_schedule/2025/10/report_card_10.html", {"request": request})


@app.get("/report_card_11", response_model=None)
async def report_card_11(request: Request):
    """
    Страница формирования табеля сотрудников ноябрь 2025 года
    """
    return templates.TemplateResponse("work_schedule/2025/11/report_card_11.html", {"request": request})


@app.get("/report_card_12", response_model=None)
async def report_card_12(request: Request):
    """
    Страница формирования табеля сотрудников декабрь 2025 года
    """
    return templates.TemplateResponse("work_schedule/2025/12/report_card_12.html", {"request": request})


@app.get("/list_employees")
async def list_employees(request: Request):
    """
    Страница списка сотрудников
    """
    try:
        employees = []
        for emp in ReportCard10.select():
            date_change = emp.date_change.strftime("%d.%m.%Y %H:%M") if emp.date_change else "—"
            employees.append({
                "ksp": emp.ksp,
                "name": emp.name,
                "category": emp.category,
                "profession": emp.profession,
                "status": emp.status,
                "abbreviation": emp.abbreviation,
                "grade": emp.grade,
                "tab": emp.tab,
                "fio": emp.fio,
                "salary": emp.salary,
                "date_change": date_change,
            })

        return templates.TemplateResponse(
            "list_employees.html",
            {"request": request, "employees": employees}
        )
    except Exception as e:
        logger.exception(e)
        return {"error": str(e)}


# CRUD операции
@app.post("/employees/", response_model=EmployeeResponse)
async def create_employee(employee: EmployeeCreate):
    new_employee = ReportCard10.create(
        name=employee.service_number,
        vacation_start=employee.vacation_start,
        vacation_end=employee.vacation_end,
    )
    return EmployeeResponse(
        id=new_employee.id,
        service_number=new_employee.service_number,
        vacation_start=new_employee.vacation_start,
        vacation_end=new_employee.vacation_end,
    )


@app.get("/employees/", response_model=List[EmployeeResponse])
async def get_employees():
    employees = ReportCard10.select()
    return [
        EmployeeResponse(
            id=emp.id,
            service_number=emp.service_number,
            vacation_start=emp.vacation_start,
            vacation_end=emp.vacation_end,
        )
        for emp in employees
    ]


@app.get("/entering_vacations", response_model=None)
async def entering_vacations(request: Request):
    """
    Страница ввода отпусков
    """
    return templates.TemplateResponse("entering_vacations.html", {"request": request})


@app.get("/")
async def index(request: Request):
    # Передаем контекст в шаблон
    # writing_employee_database()
    return templates.TemplateResponse("index.html", {"request": request})
