from tempfile import template
from fastapi import APIRouter, Form, HTTPException, Depends, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import secrets
import re

from schema.user_schema import UserRegister, UserLogin
from models.user import User
from database.database import SessionLocal
from middleware.auth import login_required

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

    # Create response with redirect
    response = RedirectResponse(url="/artgalleryproject", status_code=303)
    
    # Set session cookie
    response.set_cookie(
        key="session",
        value=secrets.token_urlsafe(32),
        httponly=True,
        max_age=1800,  # 30 minutes
        samesite="lax"
    )
    
    # Set user info in cookies
    response.set_cookie(
        key="user_id",
        value=str(user.user_id),
        httponly=True,
        max_age=1800,
        samesite="lax"
    )
    response.set_cookie(
        key="username",
        value=user.username,
        httponly=True,
        max_age=1800,
        samesite="lax"
    )
    
    return response

@router.get("/register", response_class=HTMLResponse)
def register_form(request: Request):
    return templates.TemplateResponse("auth/register.html", {"request": request, "error": None})

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

    # Validate email format
    email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    if not email_pattern.match(email):
        return templates.TemplateResponse("auth/register.html", {
            "request": request,
            "error": "❌ Please enter a valid email address."
        })

    # Check if username already exists
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        return templates.TemplateResponse("auth/register.html", {
            "request": request,
            "error": "❌ Username already taken. Please choose another."
        })

    # Check if email already exists
    existing_email = db.query(User).filter(User.email == email).first()
    if existing_email:
        return templates.TemplateResponse("auth/register.html", {
            "request": request,
            "error": "❌ Email already registered. Please use another email."
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

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        # Create response with redirect
        response = RedirectResponse(url="/artgalleryproject", status_code=303)
        
        # Set session cookie
        response.set_cookie(
            key="session",
            value=secrets.token_urlsafe(32),
            httponly=True,
            max_age=1800,  # 30 minutes
            samesite="lax"
        )
        
        # Set user info in cookies
        response.set_cookie(
            key="user_id",
            value=str(new_user.user_id),
            httponly=True,
            max_age=1800,
            samesite="lax"
        )
        response.set_cookie(
            key="username",
            value=new_user.username,
            httponly=True,
            max_age=1800,
            samesite="lax"
        )
        
        return response
    except Exception as e:
        db.rollback()
        return templates.TemplateResponse("auth/register.html", {
            "request": request,
            "error": f"❌ An error occurred during registration: {str(e)}"
        })

@router.get("/logout")
def logout():
    response = RedirectResponse(url="/artgalleryproject/auth/login", status_code=303)
    response.delete_cookie("session")
    response.delete_cookie("user_id")
    response.delete_cookie("username")
    return response

@router.get("/profile", response_class=HTMLResponse)
@login_required
async def profile_page(request: Request, db: Session = Depends(get_db)):
    user_id = request.cookies.get('user_id')
    if not user_id:
        return RedirectResponse(url="/artgalleryproject/auth/login", status_code=303)
        
    user = db.query(User).filter(User.user_id == int(user_id)).first()
    if not user:
        return RedirectResponse(url="/artgalleryproject/auth/login", status_code=303)
        
    return templates.TemplateResponse("profile.html", {
        "request": request,
        "user": user
    })

@router.post("/profile/update", response_class=HTMLResponse)
@login_required
async def update_profile(
    request: Request,
    firstName: str = Form(...),
    lastName: str = Form(...),
    email: str = Form(...),
    secondaryEmail: str = Form(None),
    db: Session = Depends(get_db)
):
    user_id = request.cookies.get('user_id')
    if not user_id:
        return RedirectResponse(url="/artgalleryproject/auth/login", status_code=303)
        
    user = db.query(User).filter(User.user_id == int(user_id)).first()
    if not user:
        return RedirectResponse(url="/artgalleryproject/auth/login", status_code=303)

    # Validate email format
    email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    if not email_pattern.match(email):
        return templates.TemplateResponse("profile.html", {
            "request": request,
            "user": user,
            "error": "❌ Please enter a valid email address."
        })

    # Validate secondary email if provided
    if secondaryEmail and not email_pattern.match(secondaryEmail):
        return templates.TemplateResponse("profile.html", {
            "request": request,
            "user": user,
            "error": "❌ Please enter a valid secondary email address."
        })

    # Check if primary email is already taken by another user
    existing_email = db.query(User).filter(User.email == email, User.user_id != user.user_id).first()
    if existing_email:
        return templates.TemplateResponse("profile.html", {
            "request": request,
            "user": user,
            "error": "❌ Email already registered. Please use another email."
        })

    # Check if secondary email is already taken by another user
    if secondaryEmail:
        existing_secondary = db.query(User).filter(
            (User.email == secondaryEmail or User.secondary_email == secondaryEmail),
            User.user_id != user.user_id
        ).first()
        if existing_secondary:
            return templates.TemplateResponse("profile.html", {
                "request": request,
                "user": user,
                "error": "❌ Secondary email already registered. Please use another email."
            })

    try:
        user.first_name = firstName.strip()
        user.last_name = lastName.strip()
        user.email = email.strip()
        user.secondary_email = secondaryEmail.strip() if secondaryEmail else None
        db.commit()
        
        return templates.TemplateResponse("profile.html", {
            "request": request,
            "user": user,
            "success": "✅ Profile updated successfully!"
        })
    except Exception as e:
        db.rollback()
        return templates.TemplateResponse("profile.html", {
            "request": request,
            "user": user,
            "error": f"❌ An error occurred: {str(e)}"
        })

@router.post("/profile/password", response_class=HTMLResponse)
@login_required
async def change_password(
    request: Request,
    currentPassword: str = Form(...),
    newPassword: str = Form(...),
    confirmPassword: str = Form(...),
    db: Session = Depends(get_db)
):
    user_id = request.cookies.get('user_id')
    if not user_id:
        return RedirectResponse(url="/artgalleryproject/auth/login", status_code=303)
        
    user = db.query(User).filter(User.user_id == int(user_id)).first()
    if not user:
        return RedirectResponse(url="/artgalleryproject/auth/login", status_code=303)

    # Verify current password
    if not check_password_hash(user.password_hash, currentPassword):
        return templates.TemplateResponse("profile.html", {
            "request": request,
            "user": user,
            "error": "❌ Current password is incorrect."
        })

    # Check if new passwords match
    if newPassword != confirmPassword:
        return templates.TemplateResponse("profile.html", {
            "request": request,
            "user": user,
            "error": "❌ New passwords do not match."
        })

    # Enforce password strength
    password_pattern = re.compile(r'^(?=.*[a-z])(?=.*\d)(?=.*[\W_]).{8,}$')
    if not password_pattern.match(newPassword):
        return templates.TemplateResponse("profile.html", {
            "request": request,
            "user": user,
            "error": "❌ Password must be at least 8 characters long and include lowercase letters, numbers, and special characters."
        })

    try:
        user.password_hash = generate_password_hash(newPassword)
        db.commit()
        
        return templates.TemplateResponse("profile.html", {
            "request": request,
            "user": user,
            "success": "✅ Password changed successfully!"
        })
    except Exception as e:
        db.rollback()
        return templates.TemplateResponse("profile.html", {
            "request": request,
            "user": user,
            "error": f"❌ An error occurred: {str(e)}"
        })
