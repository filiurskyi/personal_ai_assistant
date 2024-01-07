from urllib.parse import parse_qs, unquote

from fastapi import APIRouter, Form
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, RedirectResponse
import starlette.status as status

from fastapi_app.conf.config import templates

router = APIRouter(prefix="/login", tags=["login"])



@router.get("/tg", response_class=HTMLResponse)
async def login_tg_get(request: Request):
    return templates.TemplateResponse("login-tg.html", {"request": request})


@router.post("/tg", response_class=HTMLResponse)
async def login_tg_post(request: Request):
    try:
        data = await request.json()
        print(" get 54325345", parse_qs(unquote(data.get("initData"))))
    except Exception as e:
        print("Exception in /login/tg", e)
    # return RedirectResponse(url="login")


@router.get("/", response_class=HTMLResponse)
async def login_get(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/token", response_class=HTMLResponse)
async def login_post(request: Request, username: str = Form(...), response_class=RedirectResponse):
    # try:
    #     data = await request.json()
    #     print(data)
    # except Exception as e:
    #     print("Exception in /login", e)
    print(username)
    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie("username", username)
    return "http://127.0.0.1:8000/"

    # return templates.TemplateResponse("index.html", {"request": request})
    # return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
    # return templates.TemplateResponse("login.html", {"request": request}, status_code=status.HTTP_302_FOUND)


