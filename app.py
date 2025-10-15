# -*- coding: utf-8 -*-
import json
from datetime import date, datetime
from typing import List

from fastapi import FastAPI, Request
from fastapi import HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from loguru import logger
from pydantic import BaseModel

from database import initialize_db, ReportCard10, ReportCard11

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


@app.get("/data_10")
async def get_data():
    """Получение данных из БД октябрь 2025 года"""
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


@app.post("/data_10")
async def save_data(request: Request):
    """Сохранение данных в БД и запись даты изменения октябрь 2025 года"""
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


@app.get("/data_11")
async def get_data():
    """Получение данных из БД ноябрь 2025 года"""
    employees = []
    for emp in ReportCard11.select():
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


@app.post("/data_11")
async def save_data(request: Request):
    """Сохранение данных в БД и запись даты изменения ноябрь 2025 года"""
    new_data = await request.json()
    now = datetime.now()  # текущее время

    for row in new_data:
        emp, created = ReportCard11.get_or_create(tab=row["Таб"])
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


@app.get("/data_12")
async def get_data():
    """Получение данных из БД декабрь 2025 года"""
    employees = []
    for emp in ReportCard11.select():
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


@app.post("/data_12")
async def save_data(request: Request):
    """Сохранение данных в БД и запись даты изменения декабрь 2025 года"""
    new_data = await request.json()
    now = datetime.now()  # текущее время

    for row in new_data:
        emp, created = ReportCard11.get_or_create(tab=row["Таб"])
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


@app.get("/calendar_2025", response_model=None)
async def calendar_2025(request: Request):
    """
    Страница календаря 2025 года
    :param request: FastAPI request
    :return: templates.TemplateResponse
    """
    return templates.TemplateResponse("choosing_month.html", {"request": request})


@app.get("/forming_employee_report_card", response_model=None)
async def forming_employee_report_card(request: Request):
    """
    Формирование графика сотрудника
    :param request: FastAPI request
    :return: templates.TemplateResponse
    """
    return templates.TemplateResponse("work_schedule/forming_employee_report_card.html", {"request": request})


# === Эндпоинты для формирования графика по табельному номеру (ноябрь 2025 → ReportCard11) ===


@app.get("/api/employee/{tab}")
async def get_employee_by_tab(tab: str):
    """Получить сотрудника по табельному номеру из ноября 2025 (ReportCard11)"""
    try:
        emp = ReportCard11.get(ReportCard11.tab == tab)
        return {
            "id": emp.id,
            "tab": emp.tab,
            "fio": emp.fio,
            "ksp": emp.ksp,
            "name": emp.name,
            "category": emp.category,
            "profession": emp.profession,
            "status": emp.status,
            "abbreviation": emp.abbreviation,
            "grade": emp.grade,
            "salary": emp.salary,
            "days": json.loads(emp.days)
        }
    except ReportCard11.DoesNotExist:
        raise HTTPException(status_code=404, detail="Сотрудник с таким табельным номером не найден в ноябре 2025")


@app.put("/api/employee/{tab}")
async def update_employee_days(tab: str, request: Request):
    """Обновить график сотрудника (только days и date_change)"""
    try:
        emp = ReportCard11.get(ReportCard11.tab == tab)
    except ReportCard11.DoesNotExist:
        raise HTTPException(status_code=404, detail="Сотрудник не найден")

    try:
        data = await request.json()
        new_days = data.get("days")

        if not isinstance(new_days, list):
            raise HTTPException(status_code=400, detail="Поле 'days' должно быть списком")

        if len(new_days) != 30:
            raise HTTPException(status_code=400,
                                detail="Ноябрь 2025 имеет 30 дней. Передано: {} дней".format(len(new_days)))

        # Обновляем только days и date_change
        emp.days = json.dumps(new_days, ensure_ascii=False)
        emp.date_change = datetime.now()
        emp.save()

        return {"status": "ok", "message": "График успешно обновлён"}
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Некорректный JSON")
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail="Ошибка при сохранении")


@app.get("/")
async def index(request: Request):
    # Передаем контекст в шаблон
    return templates.TemplateResponse("index.html", {"request": request})
