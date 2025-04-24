from fastapi import FastAPI, Request, Depends, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from datetime import date
from collections import namedtuple

from models.artist import Artist
from models.collector import Collector
from models.artwork import Artwork
from models.sale import Sale
from database.database import SessionLocal
from routes.report import router as report_router

# Sub-application
gallery_app = FastAPI()

# Static files and templates
gallery_app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Routes under /artgalleryproject
@gallery_app.get("/", response_class=HTMLResponse)
def read_artists(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@gallery_app.get("/form", response_class=HTMLResponse)
def artist_form(request: Request): 
    return templates.TemplateResponse("form.html", {"request": request})

@gallery_app.get("/form/artist-form", response_class=HTMLResponse)
async def get_artist_form(request: Request):
    return templates.TemplateResponse("form/artist-info-form.html", {"request": request})

# Include additional routers
gallery_app.include_router(report_router)

# Main application
app = FastAPI()
app.mount("/artgalleryproject", gallery_app)
