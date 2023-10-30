from typing import Annotated

from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, Response

from login import login

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
    data = ""
    return login(username, password)
    

@app.get("/login.css")
async def loginCSS():
    data = ""
    with open(staticPath + "/login.css", "r")as ff:
        data = ff.read()
    return Response(content = data, media_type = CSS_MEDIA_TYPE)