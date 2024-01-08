import json
import logging
from urllib.parse import parse_qs, unquote

import starlette.status as status
from fastapi import APIRouter, Form
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, RedirectResponse

from fastapi_app.conf.config import templates
from fastapi_app.services import auth
from main import bot
router = APIRouter(prefix="/login", tags=["login"])


@router.get("/tg", response_class=HTMLResponse)
async def login_tg_get(request: Request):
    return templates.TemplateResponse("login-tg.html", {"request": request})


@router.post("/tg", response_class=HTMLResponse)
async def login_tg_post(request: Request):
    # try:
    data = await request.json()
    parsed_data = parse_qs(unquote(data.get("initData")))
    user = json.loads(parsed_data.get("user")[0])
    user_id = user.get("id")
    user_first_name = user.get("first_name")
    user_last_name = user.get("last_name")
    user_language_code = user.get("language_code")
    user_username = user.get("username")

    chat_instance = parsed_data.get("chat_instance")[0]
    chat_type = parsed_data.get("chat_type")[0]
    auth_date = parsed_data.get("auth_date")[0]
    hash_ = parsed_data.get("hash")[0]
    user_logged_in = await auth.login_check(user_id, hash_)
    if user_logged_in:
        ...
    else:
        await auth.login(user_id, hash_)
        await bot.send_message(user_id, text=f"Hello, {user_first_name}!\n\n\nYou logged in!")
    # logging.info((user_id, user_username, user_first_name, user_last_name, user_language_code))
    # logging.info((chat_instance, chat_type, auth_date, hash_))
    # except Exception as e:
    #     print("Exception in /login/tg", e)
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
    return

    # return templates.TemplateResponse("index.html", {"request": request})
    # return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
    # return templates.TemplateResponse("login.html", {"request": request}, status_code=status.HTTP_302_FOUND)
