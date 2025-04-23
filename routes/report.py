from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from models.artist import Artist
from models.collector import Collector
from database.database import SessionLocal

templates = Jinja2Templates(directory="templates")

router = APIRouter(
    prefix="/report",
    tags=["Reports"]
)

# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_class=None)
def report_home(request: Request):
    return templates.TemplateResponse("report/report-home.html", {"request": request})


@router.get("/artists", response_class=None)
def artist_report(request: Request, db: Session = Depends(get_db)):
    artists = db.query(Artist).all()
    return templates.TemplateResponse("report/artist-report.html", {"request": request, "artists": artists})


@router.get("/collectors", response_class=None)
def collector_report(request: Request, db: Session = Depends(get_db)):
    collectors = db.query(Collector).all()
    return templates.TemplateResponse("report/collector-report.html", {"request": request, "collectors": collectors})
