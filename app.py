# -*- coding: utf-8 -*-
from datetime import date
from typing import List

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from loguru import logger
from pydantic import BaseModel

from database import Employee, initialize_db

app = FastAPI()  # Создаем экземпляр FastAPI
# Монтируем статические файлы
app.mount('/static', StaticFiles(directory='static'), name='static')
# Создаем экземпляр Jinja2Templates
templates = Jinja2Templates(directory="templates")

# Инициализация БД при запуске приложения
initialize_db()


# Модели Pydantic
class EmployeeCreate(BaseModel):
    name: str
    vacation_start: date
    vacation_end: date


class EmployeeResponse(BaseModel):
    id: int
    name: str
    vacation_start: date
    vacation_end: date


@app.get("/list_employees", response_model=None)  # response_model лучше убрать
async def list_employees(request: Request):
    """
    Страница списка сотрудников
    """
    try:
        employees = []
        for emp in Employee.select():
            employees.append({
                "name": emp.name,
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
        name=employee.name,
        vacation_start=employee.vacation_start,
        vacation_end=employee.vacation_end,
    )
    return EmployeeResponse(
        id=new_employee.id,
        name=new_employee.name,
        vacation_start=new_employee.vacation_start,
        vacation_end=new_employee.vacation_end,
    )


@app.get("/employees/", response_model=List[EmployeeResponse])
async def get_employees():
    employees = Employee.select()
    return [
        EmployeeResponse(
            id=emp.id,
            name=emp.name,
            vacation_start=emp.vacation_start,
            vacation_end=emp.vacation_end,
        )
        for emp in employees
    ]


@app.get("/")
async def index(request: Request):
    # Передаем контекст в шаблон
    return templates.TemplateResponse("index.html", {"request": request})
