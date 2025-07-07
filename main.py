from fastapi import FastAPI, Form, Request, Depends
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.templating import Jinja2Templates
from models import users
from auth import hash_password,verify_password

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home(request:Request):
    return templates.TemplateResponse("login.html",{"request":request,"message":""})

@app.get("/register", response_class=HTMLResponse)
def register_page(request:Request):
    return templates.TemplateResponse("register.html",{"request":request})


@app.post("/register",response_class=HTMLResponse)
def register(email:str = Form(...),password:str=Form(...)):
    if users.find_one({"email":email}):
        return RedirectResponse(url ="/register",status_code=303)
    hashed= hash_password(password)
    users.insert_one({"email": email, "password": hashed})
    return RedirectResponse(url="/", status_code=303)

@app.post("/login")

def login(request:Request,email:str = Form(...),password:str=Form(...)):
    user = users.find_one({"email": email})
    if not user or not verify_password(password,user["password"]):
        return templates.TemplateResponse("login.html",{"request":request, "message":"Invalid Credentials"})
    return templates.TemplateResponse("main.html", {"request": request, "message": f"Welcome, {email}!"})
