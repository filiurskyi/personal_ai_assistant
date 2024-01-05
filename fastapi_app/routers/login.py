from pathlib import Path
from urllib.parse import parse_qs, unquote

from fastapi import APIRouter, HTTPException
from fastapi.requests import Request
from fastapi.responses import HTMLResponse

router = APIRouter()
from fastapi_app.config import templates


@router.get("/login-tg", response_class=HTMLResponse)
async def login_tg_get(request: Request):
    return templates.TemplateResponse("login-tg.html", {"request": request})


@router.post("/login-tg", response_class=HTMLResponse)
async def login_tg_post(request: Request):
    try:
        data = await request.json()
        print(" get ", parse_qs(unquote(data.get("initData"))))
    except Exception as e:
        print("Exception in /login-tg", e)
    # return RedirectResponse(url="login")


@router.get("/login", response_class=HTMLResponse)
async def login_get(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login", response_class=HTMLResponse)
async def login_post(request: Request):
    try:
        data = await request.json()
        print(data)
    except Exception as e:
        print("Exception in /login", e)

    return templates.TemplateResponse("index.html", {"request": request})
