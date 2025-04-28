from tempfile import template
from fastapi import APIRouter, Form, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

from schema.user_schema import UserRegister, UserLogin
from models.user import User
from database.database import SessionLocal

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


templates = Jinja2Templates(directory="templates")
# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request, "error": None})

@router.post("/login", response_class=HTMLResponse)
def login_submit(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == username).first()

    if not user or not check_password_hash(user.password_hash, password):
        return templates.TemplateResponse("auth/login.html", {"request": request, "error": "Invalid username or password"})

    user.last_login = datetime.now()
    db.commit()

    return RedirectResponse(url="/artgalleryproject", status_code=303)

@router.get("/register", response_class=HTMLResponse)
def register_form(request: Request):
    return templates.TemplateResponse("auth/register.html", {"request": request, "error": None})

from fastapi import Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
import re

@router.post("/register", response_class=HTMLResponse)
def register_submit(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    email: str = Form(...),
    first_name: str = Form(...),
    last_name: str = Form(...),
    db: Session = Depends(get_db)
):
    # Check if passwords match
    if password != confirm_password:
        return templates.TemplateResponse("auth/register.html", {
            "request": request,
            "error": "❌ Passwords do not match."
        })

    # Enforce password strength
    password_pattern = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$')
    if not password_pattern.match(password):
        return templates.TemplateResponse("auth/register.html", {
            "request": request,
            "error": "❌ Password must be at least 8 characters long and include uppercase, lowercase, number, and special character."
        })

    # Check if username already exists
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        return templates.TemplateResponse("auth/register.html", {
            "request": request,
            "error": "❌ Username already taken. Please choose another."
        })

    # Hash the password and create new user
    hashed_password = generate_password_hash(password)
    new_user = User(
        username=username.strip(),
        password_hash=hashed_password,
        email=email.strip(),
        first_name=first_name.strip(),
        last_name=last_name.strip()
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return RedirectResponse(url="/auth/login", status_code=303)
