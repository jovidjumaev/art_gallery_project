from fastapi import FastAPI, Request, Depends, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text
from sqlalchemy.orm import Session
from datetime import date

from models.artist import Artist
from models.collector import Collector
from models.artwork import Artwork
from models.sale import Sale
from database.database import SessionLocal
from collections import namedtuple
from routes.report import router as report_router 


app = FastAPI()

# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Route to show artist data
@app.get("/artgalleryproject")
def read_artists(request: Request):

    return templates.TemplateResponse("index.html", {"request": request})

@app.get("artgalleryproject/form")
def artist_form(request: Request): 
    return templates.TemplateResponse("form.html", {"request": request})


@app.get("/form/artist-form", response_class=HTMLResponse)
async def get_artist_form(request: Request):
    return templates.TemplateResponse("/form/artist-info-form.html", {"request": request})


app.include_router(report_router)