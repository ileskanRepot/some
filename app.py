from typing import Annotated

from fastapi import Cookie, FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from starlette.status import HTTP_302_FOUND,HTTP_303_SEE_OTHER

from login import login, isLoggedIn

app = FastAPI()

staticPath = "./static"

CSS_MEDIA_TYPE = "text/css"
HTML_MEDIA_TYPE = "text/html"


@app.get("/")
async def homepage():
    data = ""
    with open(staticPath + "/index.html", "r")as ff:
        data = ff.read()
    return Response(content = data, media_type = HTML_MEDIA_TYPE)

@app.get("/index.css")
async def homecss():
    data = ""
    with open(staticPath + "/index.css", "r")as ff:
        data = ff.read()
    return Response(content = data, media_type = CSS_MEDIA_TYPE)

@app.get("/login")
async def loginGet():
    data = ""
    with open(staticPath + "/login.html", "r")as ff:
        data = ff.read()
    return Response(content = data, media_type = HTML_MEDIA_TYPE)

@app.post("/login")
async def loginPost(username: Annotated[str, Form()],password: Annotated[str, Form()]):
    loginStatus,cookie = login(username, password)
    if not loginStatus:
        return RedirectResponse("/login",status_code=HTTP_302_FOUND)
    retVal = RedirectResponse("/",status_code=HTTP_302_FOUND)
    retVal.set_cookie(key="cookie",value=cookie)
    retVal.set_cookie(key="username",value=username)
    return retVal
    

@app.get("/login.css")
async def loginCSS():
    data = ""
    with open(staticPath + "/login.css", "r")as ff:
        data = ff.read()
    return Response(content = data, media_type = CSS_MEDIA_TYPE)

@app.get("/secret")
async def secret(username: str = Cookie(default = ""),cookie: str = Cookie(default = "")):
    if not isLoggedIn(username,cookie):
        return Response(content = "NOT AUTENTICATED", media_type = HTML_MEDIA_TYPE)
    
    return Response(content = "YOU GOT SECRET", media_type = HTML_MEDIA_TYPE)