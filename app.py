# -*- coding: utf-8 -*-
from datetime import date
from typing import List
import json
from pathlib import Path
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from loguru import logger
from pydantic import BaseModel

from database import Employee, initialize_db, writing_employee_database

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


DATA_FILE = Path("data.json")


@app.get("/data")
async def get_data():
    """Возвращаем данные из JSON"""
    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return JSONResponse(content=data)
    return JSONResponse(content=[], status_code=200)


@app.post("/data")
async def save_data(new_data: list):
    """Сохраняем данные в JSON"""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(new_data, f, ensure_ascii=False, indent=4)
    return {"status": "ok"}


@app.get("/report_card", response_model=None)
async def report_card(request: Request):
    """Страница формирования табеля сотрудников"""
    return templates.TemplateResponse("report_card.html", {"request": request})


@app.get("/list_employees", response_model=None)  # response_model лучше убрать
async def list_employees(request: Request):
    """
    Страница списка сотрудников
    """
    try:
        employees = []
        for emp in Employee.select():
            employees.append({
                "service_number": emp.service_number,
                "vacation_start": emp.vacation_start,
                "vacation_end": emp.vacation_end,
            })

        return templates.TemplateResponse(
            "list_employees.html",
            {"request": request, "employees": employees}
        )
    except Exception as e:
        logger.exception(e)


# CRUD операции
@app.post("/employees/", response_model=EmployeeResponse)
async def create_employee(employee: EmployeeCreate):
    new_employee = Employee.create(
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
    employees = Employee.select()
    return [
        EmployeeResponse(
            id=emp.id,
            service_number=emp.service_number,
            vacation_start=emp.vacation_start,
            vacation_end=emp.vacation_end,
        )
        for emp in employees
    ]


@app.get("/")
async def index(request: Request):
    # Передаем контекст в шаблон
    writing_employee_database()
    return templates.TemplateResponse("index.html", {"request": request})
