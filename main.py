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
@app.get("/")
def read_artists(request: Request):

    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/active-artists")
def read_artists(request: Request, db: Session = Depends(get_db)):
    artists = db.query(Artist).all()
    today = date.today()
    return templates.TemplateResponse("active-artist.html", {"request": request, "artists": artists, "today":today})

@app.get("/individual-collector-sale")
def individual_collector(request: Request, db: Session = Depends(get_db)):
    collector = db.query(Collector).all()
    return templates.TemplateResponse("individual-collector-sale.html", {"request": request, "artists": collector})

# @app.get('/work-for-sale')
# def work_for_sale(request: Request,db: Session = Depends(get_db)): 

    

@app.get("/report")
def get_artists(request: Request):
    return templates.TemplateResponse("report.html", {"request": request})


@app.get("/form")
def artist_form(request: Request): 
    return templates.TemplateResponse("form.html", {"request": request})


@app.get("/form/artist-form", response_class=HTMLResponse)
async def get_artist_form(request: Request):
    return templates.TemplateResponse("/form/artist-info-form.html", {"request": request})


@app.get('/work-for-sale')
def work_for_sale(
    request: Request,
    db: Session = Depends(get_db),
    collector_ssn: str = Query(..., description="Collector SSN to filter")
):
    start_date = date(2022, 1, 1)
    end_date = date(2025, 12, 31)

    raw_results = (
        db.query(
            Artwork.worktitle,
            Artwork.artistid,
            Artwork.datelisted,
            Artwork.worktype,
            Artwork.workmedium,
            Artwork.workstyle,
            Artwork.workyearcompleted,
            Artwork.askingprice,
            Sale.saleprice,
            Sale.saledate
        )
        .join(Sale, Artwork.artworkid == Sale.artworkid)
        .filter(Artwork.collectorsocialsecuritynumber == collector_ssn)
        .filter(Artwork.datelisted.between(start_date, end_date))
        .all()
    )

    WorkSale = namedtuple("WorkSale", [
        "worktitle", "artistid", "datelisted", "worktype", "workmedium",
        "workstyle", "workyearcompleted", "askingprice", "saleprice", "saledate"
    ])

    results = [WorkSale(*row) for row in raw_results]

    return templates.TemplateResponse("work-for-sale.html", {
        "request": request,
        "results": results,
        "collector_ssn": collector_ssn
    })