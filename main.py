from fastapi import FastAPI, Request, Depends, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from datetime import date
from collections import namedtuple
from starlette.exceptions import HTTPException as StarletteHTTPException
from middleware.auth import AuthMiddleware

from models.artist import Artist
from models.collector import Collector
from models.artwork import Artwork
from models.sale import Sale
from database.database import SessionLocal

from routes.report import router as report_router
from routes.form import router as form_router
from routes.auth import router as auth_router


# Sub-application
gallery_app = FastAPI()

# Static files and templates
gallery_app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Apply authentication middleware to all routes
gallery_app.add_middleware(AuthMiddleware)

@gallery_app.get("/", response_class=HTMLResponse)
async def read_artists(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@gallery_app.exception_handler(404)
async def not_found(request: Request, exc: StarletteHTTPException):
    return templates.TemplateResponse("404.html", {"request": request}, status_code=404)

@gallery_app.get('/about', response_class=HTMLResponse)
async def about_me(request: Request): 
    return templates.TemplateResponse("about.html", {"request": request})

# Include additional routers
gallery_app.include_router(report_router)
gallery_app.include_router(form_router)
gallery_app.include_router(auth_router)


# Main application
app = FastAPI()
app.mount("/artgalleryproject", gallery_app)



