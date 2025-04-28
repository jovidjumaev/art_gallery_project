from collections import namedtuple
from fastapi import APIRouter, Query, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import date, timedelta

from models.artist import Artist
from models.collector import Collector
from models.artwork import Artwork
from models.sale import Sale
from models.buyer import Buyer
from models.artshow import ArtShow
from models.shownin import ShownIn
from models.salesperson import Salesperson
from database.database import SessionLocal
from decimal import Decimal
from urllib.parse import unquote


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

#Main page
@router.get("/")
def get_artists(request: Request):
    return templates.TemplateResponse("report.html", {"request": request})

#Active Artists Summary Report
@router.get("/active-artists")
def read_artists(request: Request, db: Session = Depends(get_db)):
    artists = db.query(Artist).all()
    today = date.today()
    return templates.TemplateResponse("/reports/active-artist.html", {"request": request, "artists": artists, "today":today})

#F
@router.get("/individual-collector-sale")
def individual_collector(request: Request, db: Session = Depends(get_db)):
    collector = db.query(Collector).all()
    return templates.TemplateResponse("/reports/individual-collector-sale.html", {"request": request, "collectors": collector})

@router.get('/individual-artist')
def individual_artist(request: Request, db: Session = Depends(get_db)): 
    artist = db.query(Artist).all()
    return templates.TemplateResponse("/artist-report-form.html", {"request": request, "artists": artist})

# @router.post("/individual-artist-sale")
# def get_individual_sale(
#     request: Request, 
#     db: Session = Depends(get_db),
#     artist_id: str = Query(..., description="Artist ID to filter")
# ):
#     # === Works Sold ===
#     sold_artworks_raw = (
#         db.query(
#             Artwork.worktitle,
#             Artwork.datelisted,
#             Artwork.worktype,
#             Artwork.workmedium,
#             Artwork.workstyle,
#             Artwork.workyearcompleted,
#             Artwork.askingprice,
#             Sale.saleprice,
#             Sale.saledate
#         )
#         .join(Sale, Artwork.artworkid == Sale.artworkid)
#         .filter(Artwork.artistid == artist_id)
#         .all()
#     )

#     SoldArtwork = namedtuple("SoldArtwork", [
#         "worktitle", "datelisted", "worktype", "workmedium",
#         "workstyle", "workyearcompleted", "askingprice", "saleprice", "saledate"
#     ])
#     sold_artworks = [SoldArtwork(*row) for row in sold_artworks_raw]
#     total_sales = sum(work.saleprice or 0 for work in sold_artworks)

#     # === Works Returned (status = 'sold') ===
#     returned_works_raw = (
#         db.query(
#             Artwork.worktitle,
#             Artwork.datelisted,
#             Artwork.worktype,
#             Artwork.workmedium,
#             Artwork.workstyle,
#             Artwork.workyearcompleted,
#             Artwork.askingprice, 
#             Artwork.datereturned,
#         )
#         .filter(Artwork.artistid == artist_id)
#         .filter(Artwork.status == "returned")
#         .all()
#     )

#     ReturnedWork = namedtuple("ReturnedWork", [
#         "worktitle", "datelisted", "worktype", "workmedium",
#         "workstyle", "workyearcompleted", "askingprice", "datereturned"
#     ])
#     returned_artworks = [ReturnedWork(*row) for row in returned_works_raw]

#     # === Works For Sale ===
#     for_sale_works_raw = (
#         db.query(
#             Artwork.worktitle,
#             Artwork.datelisted,
#             Artwork.worktype,
#             Artwork.workmedium,
#             Artwork.workstyle,
#             Artwork.workyearcompleted,
#             Artwork.askingprice
#         )
#         .filter(Artwork.artistid == artist_id)
#         .filter(Artwork.status == "for sale")
#         .all()
#     )

#     ForSaleArtwork = namedtuple("ForSaleArtwork", [
#         "worktitle", "datelisted", "worktype", "workmedium",
#         "workstyle", "workyearcompleted", "askingprice"
#     ])
#     for_sale_artworks = [ForSaleArtwork(*row) for row in for_sale_works_raw]
#     total_asking_price = sum(work.askingprice or 0 for work in for_sale_artworks)

#     return templates.TemplateResponse("/artist-report.html", {
#         "request": request,
#         "artist_id": artist_id,
#         "sold_works": sold_artworks,
#         "total_sales": total_sales,
#         "returned_works": returned_artworks,
#         "forSale_works": for_sale_artworks,
#         "total_asking_price": total_asking_price
#     })


@router.get('/work-for-sale')
def work_for_sale(
    request: Request,
    db: Session = Depends(get_db)
):
    raw_results = (
        db.query(
            Artwork.worktitle,
            Artist.firstname.label("artist_firstname"),
            Artist.lastname.label("artist_lastname"),
            Artwork.worktype,
            Artwork.workmedium,
            Artwork.workstyle,
            Collector.firstname.label("owner_firstname"),
            Collector.lastname.label("owner_lastname"),
            Artwork.askingprice,
            Artwork.dateshown,
            Artwork.datelisted
        )
        .join(Artist, Artwork.artistid == Artist.artistid)
        .outerjoin(Collector, Artwork.collectorsocialsecuritynumber == Collector.socialsecuritynumber)  # <<< OUTER JOIN
        .filter(Artwork.status == 'for sale')
        .all()
    )

    WorkForSale = namedtuple("WorkForSale", [
        "worktitle", "artist_firstname", "artist_lastname", "worktype",
        "workmedium", "workstyle", "owner_firstname", "owner_lastname",
        "askingprice", "dateshown", "datelisted"
    ])

    results = [WorkForSale(*row) for row in raw_results]

    return templates.TemplateResponse("/reports/work-for-sale.html", {
        "request": request,
        "results": results
    })


#Collectors Summary Report
@router.get("/collector-summary")
def get_collector_summary(request: Request, db: Session = Depends(get_db)):
    raw_results = (
        db.query(
            Collector.firstname.label("collector_firstname"),
            Collector.lastname.label("collector_lastname"),
            Collector.street.label("street"),
            Collector.zip.label("zip"),
            Collector.telephonenumber.label("phone"),
            Collector.collectionartistid.label("preferred_artist"),
            Collector.collectiontype.label("preferred_type"),
            Collector.collectionmedium.label("preferred_medium"),
            Collector.collectionstyle.label("preferred_style"),
            Collector.saleslastyear.label("sales_last_year"),
            Collector.salesyeartodate.label("sales_ytd")
        ).all()
    )

    CollectorSummary = namedtuple("CollectorSummary", [
        "collector_firstname", "collector_lastname", "street", "zip", "phone",
        "preferred_artist", "preferred_type", "preferred_medium", "preferred_style",
        "sales_last_year", "sales_ytd"
    ])

    collectors = [CollectorSummary(*row) for row in raw_results]

    return templates.TemplateResponse("/reports/collector-summary.html", {
        "request": request,
        "collectors": collectors
    })

@router.get("/sales-this-week")
def get_sale_this_week(request: Request, db: Session = Depends(get_db)):
   
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())  # Monday
    end_of_week = start_of_week + timedelta(days=6)          # Sunday
    # start_of_week= '24-MAR-2025'
    # end_of_week = '30-MAR-2025'

    # Query individual sales
    raw_results = (
        db.query(
            Salesperson.firstname.label("salesperson_firstname"),
            Salesperson.lastname.label("salesperson_lastname"),
            Artist.firstname.label("artist_firstname"),
            Artist.lastname.label("artist_lastname"),
            Artwork.worktitle.label("work_title"),
            Collector.firstname.label("owner_firstname"),
            Collector.lastname.label("owner_lastname"),
            Buyer.firstname.label("buyer_firstname"),
            Buyer.lastname.label("buyer_lastname"),
            Sale.saledate.label("sale_date"),
            Sale.saleprice.label("selling_price")
        )
        .join(Salesperson, Sale.salespersonssn == Salesperson.socialsecuritynumber)
        .join(Artwork, Sale.artworkid == Artwork.artworkid)
        .join(Artist, Artwork.artistid == Artist.artistid)
        .join(Buyer, Sale.buyerid == Buyer.buyerid)
        .filter(Sale.saledate.between(start_of_week, end_of_week))
        .outerjoin(Collector, Artwork.collectorsocialsecuritynumber == Collector.socialsecuritynumber)
        .order_by(Salesperson.lastname, Salesperson.firstname)
        .all()
    )

    SaleThisWeek = namedtuple("SaleThisWeek", [
        "salesperson_firstname", "salesperson_lastname",
        "artist_firstname", "artist_lastname",
        "work_title",
        "owner_firstname", "owner_lastname",
        "buyer_firstname", "buyer_lastname",
        "sale_date", "selling_price", "commission"
    ])

    sales = [
        SaleThisWeek(
            *row,
            row.selling_price * Decimal("0.05") if row.selling_price else Decimal("0.0")
        )
        for row in raw_results
    ]

    # Query total sales and total commission
    total_result = db.query(
        Sale.saleprice
    ).filter(Sale.saledate.between(start_of_week, end_of_week)).all()

    grand_total_sales = sum([r.saleprice for r in total_result if r.saleprice])
    grand_total_commission = grand_total_sales * Decimal("0.05")

    return templates.TemplateResponse("/reports/sales-this-week.html", {
        "request": request,
        "sales": sales,
        "start_date": start_of_week,
        "end_date": end_of_week,
        "grand_total_sales": grand_total_sales,
        "grand_total_commission": grand_total_commission
    })

@router.get("/aged-artworks")
def get_aged_artworks(request: Request, db: Session = Depends(get_db)):
    # Set the cutoff date for 6 months ago from today
    today = date.today()
    six_months_ago = today - timedelta(days=6*30)  # Rough approximation for 6 months
    formatted_date = today.strftime("%m/%d/%Y")
    # Query for aged artworks still for sale
    raw_results = (
        db.query(
            Collector.firstname.label("collector_firstname"),
            Collector.lastname.label("collector_lastname"),
            Collector.areacode.label("area_code"),
            Collector.telephonenumber.label("collector_phone"),
            Artist.firstname.label("artist_firstname"),
            Artist.lastname.label("artist_lastname"),
            Artwork.worktitle.label("work_title"),
            Artwork.datelisted.label("date_listed"),
            Artwork.askingprice.label("asking_price")
        )
        .join(Artist, Artwork.artistid == Artist.artistid)
        .outerjoin(Collector, Artwork.collectorsocialsecuritynumber == Collector.socialsecuritynumber)
        .filter(
            Artwork.status == 'for sale',
            Artwork.datelisted <= six_months_ago
        )
        .order_by(Collector.lastname, Collector.firstname, Artwork.datelisted)
        .all()
    )

    AgedArtwork = namedtuple("AgedArtwork", [
        "collector_firstname", "collector_lastname",
        "area_code", "collector_phone",
        "artist_firstname", "artist_lastname",
        "work_title", "date_listed", "asking_price"
    ])

    aged_artworks = [AgedArtwork(*row) for row in raw_results]

    return templates.TemplateResponse("/reports/aged-artworks.html", {
        "request": request,
        "aged_artworks": aged_artworks,
        "cutoff_date": six_months_ago,
        "todayDate": formatted_date
    })

@router.get("/show-details")
def get_show_details(
    request: Request,
    db: Session = Depends(get_db)
):
    result_raw = (
        db.query(
            ArtShow.showtitle.label("show_title"),
            ArtShow.showopeningdate.label("opening_date"),
            ArtShow.showclosingdate.label("closing_date"),
            Artist.firstname.label("featured_artist_firstname"),
            Artist.lastname.label("featured_artist_lastname"),
            ArtShow.showtheme.label("theme")
        )
        .join(Artist, ArtShow.showfeaturedartistid == Artist.artistid)
        .all()
    )

    ShowDetails = namedtuple("ShowDetails", [
        "show_title", "opening_date", "closing_date",
        "featured_artist_firstname", "featured_artist_lastname", "theme"
    ])

    show_info = [ShowDetails(*row) for row in result_raw]

    return templates.TemplateResponse("/reports/show-details.html", {
        "request": request,
        "shows": show_info
    })

@router.get("/show-artworks/{show_title}")
def get_show_artworks(
    request: Request,
    show_title: str,
    db: Session = Depends(get_db)
):
    # Decode and clean up the title
    decoded_title = unquote(show_title).strip()

    raw_results = (
        db.query(
            Artist.firstname.label("artist_firstname"),
            Artist.lastname.label("artist_lastname"),
            Artwork.worktitle.label("title"),
            Artwork.askingprice,
            Artwork.status
        )
        .join(Artwork, Artwork.artistid == Artist.artistid)
        .join(ShownIn, ShownIn.artworkid == Artwork.artworkid)
        .filter(ShownIn.showtitle.ilike(decoded_title))
        .all()
    )

    ShowArtwork = namedtuple("ShowArtwork", [
        "artist_firstname", "artist_lastname", "title", "askingprice", "status"
    ])

    artworks = [ShowArtwork(*row) for row in raw_results]

    return templates.TemplateResponse("/reports/art-show-details.html", {
        "request": request,
        "artworks": artworks,
        "show_title": decoded_title
    })


@router.get("/artist-report-form")
def artist_report_form(request: Request, db: Session = Depends(get_db)):
    artists = db.query(Artist).all()
    today = date.today()
    end_of_year = date(today.year, 12, 31)

    return templates.TemplateResponse("artist-report-form.html", {
        "request": request,
        "artists": artists,
        "today": today,
        "end_of_year": end_of_year
    })

@router.post("/indivudal-artists-sale")
def generate_artist_report(
    request: Request,
    db: Session = Depends(get_db),
    start_date: date = Form(...),
    end_date: date = Form(...),
    artist_id: int = Form(...)
):
    # Get artist info
    artist = db.query(Artist).filter(Artist.artistid == artist_id).first()

    # Get artworks listed during that time
    artworks = (
        db.query(Artwork)
        .filter(
            Artwork.artistid == artist_id,
            Artwork.datelisted >= start_date,
            Artwork.datelisted <= end_date
        )
        .all()
    )

    return templates.TemplateResponse("artist-report.html", {
        "request": request,
        "artist": artist,
        "artworks": artworks,
        "start_date": start_date,
        "end_date": end_date
    })


@router.post("/individual-artist-sale")
def get_individual_sale(
    request: Request,
    db: Session = Depends(get_db),
    artist_id: str = Form(...),   # 🔥 Change from Query to Form
    start_date: str = Form(...),   # 🔥 Accept start_date (you had it in your form)
    end_date: str = Form(...)      # 🔥 Accept end_date (hidden input in your form)
):
    # === Works Sold ===
    sold_artworks_raw = (
        db.query(
            Artwork.worktitle,
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
        .filter(Artwork.artistid == artist_id)
        .filter(Sale.saledate >= start_date)   # 🔥 filter by date range
        .filter(Sale.saledate <= end_date)
        .all()
    )

    SoldArtwork = namedtuple("SoldArtwork", [
        "worktitle", "datelisted", "worktype", "workmedium",
        "workstyle", "workyearcompleted", "askingprice", "saleprice", "saledate"
    ])
    sold_artworks = [SoldArtwork(*row) for row in sold_artworks_raw]
    total_sales = sum(work.saleprice or 0 for work in sold_artworks)

    # === Works Returned ===
    returned_works_raw = (
        db.query(
            Artwork.worktitle,
            Artwork.datelisted,
            Artwork.worktype,
            Artwork.workmedium,
            Artwork.workstyle,
            Artwork.workyearcompleted,
            Artwork.askingprice,
            Artwork.datereturned,
        )
        .filter(Artwork.artistid == artist_id)
        .filter(Artwork.status == "returned")
        .all()
    )

    ReturnedWork = namedtuple("ReturnedWork", [
        "worktitle", "datelisted", "worktype", "workmedium",
        "workstyle", "workyearcompleted", "askingprice", "datereturned"
    ])
    returned_artworks = [ReturnedWork(*row) for row in returned_works_raw]

    # === Works For Sale ===
    for_sale_works_raw = (
        db.query(
            Artwork.worktitle,
            Artwork.datelisted,
            Artwork.worktype,
            Artwork.workmedium,
            Artwork.workstyle,
            Artwork.workyearcompleted,
            Artwork.askingprice
        )
        .filter(Artwork.artistid == artist_id)
        .filter(Artwork.status == "for sale")
        .all()
    )

    ForSaleArtwork = namedtuple("ForSaleArtwork", [
        "worktitle", "datelisted", "worktype", "workmedium",
        "workstyle", "workyearcompleted", "askingprice"
    ])
    for_sale_artworks = [ForSaleArtwork(*row) for row in for_sale_works_raw]
    total_asking_price = sum(work.askingprice or 0 for work in for_sale_artworks)

    return templates.TemplateResponse("/artist-report.html", {
        "request": request,
        "artist_id": artist_id,
        "sold_works": sold_artworks,
        "total_sales": total_sales,
        "returned_works": returned_artworks,
        "forSale_works": for_sale_artworks,
        "total_asking_price": total_asking_price
    })


