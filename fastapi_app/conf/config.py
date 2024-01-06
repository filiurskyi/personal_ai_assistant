from os import getenv
from pathlib import Path

from dotenv import load_dotenv
from fastapi import APIRouter
from fastapi.templating import Jinja2Templates

BASE_DIR = Path(__file__).parent

STATIC_PATH = BASE_DIR.parent / "static"
TEMPLATES = BASE_DIR.parent / "templates"
templates = Jinja2Templates(directory=TEMPLATES)

router = APIRouter()

load_dotenv(dotenv_path=str(BASE_DIR.parent.parent / ".env"))

# DB_URI = "sqlite+aiosqlite:///database.db/"
DB_URI = f"postgresql+asyncpg://{getenv('PG_USER')}:{getenv('PG_PWD')}@{getenv('PG_HOST')}:{getenv('PG_PORT')}/{getenv('PG_DB_NAME')}"
print(DB_URI)