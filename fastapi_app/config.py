from pathlib import Path

from fastapi import APIRouter
from fastapi.templating import Jinja2Templates

BASE_DIR = Path(__file__).parent


STATIC_PATH = BASE_DIR / "static"
TEMPLATES = BASE_DIR / "templates"
print(TEMPLATES)
templates = Jinja2Templates(directory=TEMPLATES)

router = APIRouter()

DB_URI = "sqlite+aiosqlite:///database.db/"
