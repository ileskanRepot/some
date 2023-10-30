import random
import string

from hashlib import sha512
from base64 import b64encode

PSW_FILE = "./psw/login.csv"

def randomStr(len):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(len))

def hash(stri,salt):
    mm = sha512()
    mm.update((stri + "," + salt).encode())
    return mm.hexdigest()

def pswLineShoudBe(username,passowrd,salt):
    return (b"\n" + b64encode(username.encode()) + b","+ b64encode(hash(passowrd,salt).encode()) + b"," + salt.encode()).decode()

def createUser(username,passowrd):
    salt = randomStr(8)
    with open(PSW_FILE, "a") as myfile:
        myfile.write(pswLineShoudBe(username, passowrd, salt))

def login(username, password):
    pswFileContent = ""
    with open(PSW_FILE, "r") as ff:
        pswFileContent = ff.read()
    for line in pswFileContent.split("\n"):
        if line.count(",") != 2:
            continue
        fileUsername, b, salt = line.split(",")

        if b64encode(username.encode()).decode() == fileUsername and pswLineShoudBe(username, password, salt)[1:] == line:
            print("authenticatoin sucseeded")

    return 123