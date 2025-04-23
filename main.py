from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from models.artist import Artist
from database.database import SessionLocal

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
@app.get("/")
def read_artists(request: Request):

    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/artists")
def read_artists(request: Request, db: Session = Depends(get_db)):
    artists = db.query(Artist).all()
    
    return templates.TemplateResponse("artist.html", {"request": request, "artists": artists})

@app.get("/report")
def get_artists(request: Request):
    return templates.TemplateResponse("report.html", {"request": request})

@app.get("/form")
def artist_form(request: Request): 
    return templates.TemplateResponse("form.html", {"request": request})


@app.get("/form/artist-form", response_class=HTMLResponse)
async def get_artist_form(request: Request):
    return templates.TemplateResponse("form/artist-info-form.html", {"request": request})