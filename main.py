from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Монтируем статические файлы
app.mount('/static', StaticFiles(directory='static'), name='static')

# Создаем экземпляр Jinja2Templates
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def index(request: Request):
    # Передаем контекст в шаблон
    return templates.TemplateResponse("index.html", {"request": request})
