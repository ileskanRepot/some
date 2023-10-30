import random
import string

from hashlib import sha512
from base64 import b64encode
from secrets import token_urlsafe
from time import time

PSW_FILE = "./psw/login.csv"
COOKIE_FILE = "./psw/cookies.csv"
SALT_LEN = 8
COOKIE_LEN = 16
SESSION_LEN = 60 * 5 # In seconds

def randomStr(len):
    return token_urlsafe(len)

def hash(stri,salt):
    mm = sha512()
    mm.update((stri + "," + salt).encode())
    return mm.hexdigest()

def pswLineShoudBe(username,passowrd,salt):
    return (b"\n" + b64encode(username.encode()) + b","+ b64encode(hash(passowrd,salt).encode()) + b"," + salt.encode()).decode()

def createUser(username,passowrd):
    salt = randomStr(SALT_LEN)
    with open(PSW_FILE, "a") as myfile:
        myfile.write(pswLineShoudBe(username, passowrd, salt))

def writeCookie(username:str) -> str:
    cookie = b64encode(randomStr(COOKIE_LEN).encode()).decode()
    with open(COOKIE_FILE,"a") as ff:
            ff.write("\n" + b64encode(username.encode()).decode() + "," + cookie + "," + str(round(time())))
    return cookie

def login(username:str, password:str) -> (bool,str):
    pswFileContent = ""
    success = False
    cookie = ""
    with open(PSW_FILE, "r") as ff:
        pswFileContent = ff.read()
    for line in pswFileContent.split("\n"):
        if line.count(",") != 2:
            continue
        fileUsername, b, salt = line.split(",")

        if b64encode(username.encode()).decode() == fileUsername and pswLineShoudBe(username, password, salt)[1:] == line:
            success = True
            cookie = writeCookie(username)
            break

    return (success,cookie)

def updateTime(username:str,cookie:str)-> None:
    cookieFileContent = ""
    with open(COOKIE_FILE, "r") as ff:
        cookieFileContent = ff.read()

    tmpContent = cookieFileContent.split("\n")
    for ii,line in enumerate(tmpContent):
        if line.count(",") != 2:
            continue
        fileUsername, fileCookie, timeStamp = line.split(",")
        print(fileCookie)
        print(cookie)
        if b64encode(username.encode()).decode() != fileUsername or cookie != fileCookie:
            continue
        tmpContent[ii] = b64encode(username.encode()).decode() + "," + cookie + "," + str(round(time()))
        break
    with open(COOKIE_FILE, "w") as ff:
        ff.write("\n".join(tmpContent))
        # cookieFileContent = ff.read()

def isLoggedIn(username:str, cookie:str) -> bool:
    clearOldCookies()
    cookieFileContent = ""
    retVal = False
    with open(COOKIE_FILE, "r") as ff:
        cookieFileContent = ff.read()
    for line in cookieFileContent.split("\n"):
        if line.count(",") != 2:
            continue
        fileUsername, fileCookie, timeStamp = line.split(",")
        if b64encode(username.encode()).decode() == fileUsername and cookie == fileCookie and int(timeStamp) > round(time()) - SESSION_LEN:
            updateTime(username, cookie)
            retVal = True
    return retVal

def clearOldCookies() -> None:
    cookieFileContent = ""
    with open(COOKIE_FILE, "r") as ff:
        cookieFileContent = ff.read()

    writeBack = []
    for ii,line in enumerate(cookieFileContent.split("\n")):
        if line.count(",") != 2:
            continue
        fileUsername, fileCookie, timeStamp = line.split(",")
        if int(timeStamp) < round(time()) - SESSION_LEN:
            continue
        writeBack.append(fileUsername + "," + fileCookie + "," + timeStamp)
        break
    print(writeBack)

    with open(COOKIE_FILE, "w") as ff:
        ff.write("\n".join(writeBack))