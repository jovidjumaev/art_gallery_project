from decimal import ROUND_HALF_UP, Decimal
from typing import Optional
from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from oracledb import DataError, IntegrityError
from datetime import datetime

import oracledb
from sqlalchemy import func
from sqlalchemy.orm import Session 
from database.database import SessionLocal
from schema.artist_schema import ArtistRequest
from schema.collector_schema import CollectorRequest
from schema.artwork_schema import ArtworkRequest
from schema.artwork_sale_schema import ArtworkSaleRequest
from schema.mailing_list_schema import MailingListRequest
from pydantic import BaseModel, Field
from models.artist import Artist
from models.collector import Collector
from models.artwork import Artwork
from models.potential_customer import PotentialCustomer

from models.sale import Sale
from models.buyer import Buyer
from models.artshow import ArtShow
from models.shownin import ShownIn
from models.salesperson import Salesperson
from models.zips import ZIPS

templates = Jinja2Templates(directory="templates")

router = APIRouter(
    prefix="/form",
    tags=["Form"]
)

today = datetime.now().strftime('%Y-%m-%d')  # Get current date for all responses

# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_class=HTMLResponse)
def artist_form(request: Request): 
    return templates.TemplateResponse("form.html", {"request": request})

@router.get("/artist-form", response_class=HTMLResponse)
def get_artist_form(request: Request):
    today = datetime.now().strftime('%Y-%m-%d')
    return templates.TemplateResponse("/form/artist-info-form.html", {"request": request, "today": today})

# GET: display artist form page
@router.get("/add-artist", response_class=HTMLResponse)
def get_artist_form(request: Request):
    return templates.TemplateResponse("/form/artist-info-form.html", {"request": request})

@router.post("/artist-form", response_class=HTMLResponse)
async def add_artist(
    request: Request,
    db: Session = Depends(get_db),
    artist_request: ArtistRequest = Depends(ArtistRequest.as_form)
):
    try:
        interview_date_obj = datetime.strptime(artist_request.interviewDate.strip(), "%Y-%m-%d")
        if artist_request.usualMedium.lower() == "other" and artist_request.otherMedium:
            artist_request.usualMedium = artist_request.otherMedium.strip()
        if artist_request.usualStyle.lower() == "other" and artist_request.otherStyle:
            artist_request.usualStyle = artist_request.otherStyle.strip()
        if artist_request.usualType.lower() == "other" and artist_request.otherType:
            artist_request.usualType = artist_request.otherType.strip()

        # Validate lengths manually (your model limits)
        if len(artist_request.usualMedium) > 15 or len(artist_request.usualStyle) > 15 or len(artist_request.usualType) > 20:
            return templates.TemplateResponse("/form/artist-info-form.html", {
                "request": request,
                "error": "❌ Medium, Style, or Type exceeds allowed length."
            })

        # Check if SSN already exists (duplicate)
        existing_artist = db.query(Artist).filter_by(socialsecuritynumber=artist_request.socialSecurityNumber).first()
        if existing_artist:
            return templates.TemplateResponse("/form/artist-info-form.html", {
                "request": request,
                "error": "❌ This SSN already exists. Please use a unique value."
            })

        # Insert new artist
        new_artist = Artist(
            firstname=artist_request.firstName.strip(),
            lastname=artist_request.lastName.strip(),
            interviewdate=interview_date_obj,
            interviewername=artist_request.interviewerName.strip(),
            street=artist_request.street.strip(),
            zip=artist_request.zip.strip(),
            areacode=artist_request.areaCode.strip(),
            telephonenumber=artist_request.telephoneNumber.strip(),
            socialsecuritynumber=artist_request.socialSecurityNumber.strip(),
            usualmedium=artist_request.usualMedium.strip(),
            usualstyle=artist_request.usualStyle.strip(),
            usualtype=artist_request.usualType.strip(),
            saleslastyear=0,
            salesyeartodate=0
        )

        db.add(new_artist)
        db.commit()

        return templates.TemplateResponse("/form/artist-info-form.html", {
            "request": request,
            "success": True
        })

    except (IntegrityError, DataError) as e:
        db.rollback()
        return templates.TemplateResponse("/form/artist-info-form.html", {
            "request": request,
            "error": "❌ Database error: Maybe a field too long or duplicate SSN."
        })
    except Exception as e:
        db.rollback()
        return templates.TemplateResponse("/form/artist-info-form.html", {
            "request": request,
            "error": f"❌ Unexpected Error: {str(e)}"
        })
    

@router.get('/collector-form')
async def get_collector(request: Request):
    today = datetime.now().strftime('%Y-%m-%d')
    return templates.TemplateResponse("/form/collector-info-form.html", {"request": request, "today": today})

@router.post('/add-collector', response_class=HTMLResponse)
async def add_collector(
    request: Request,
    db: Session = Depends(get_db),
    collector_request: CollectorRequest = Depends(CollectorRequest.as_form)
):
    today = datetime.now().strftime('%Y-%m-%d')  # Get current date for all responses
    try:
        # Validate interview date
        if not collector_request.interviewDate:
            return templates.TemplateResponse("/form/collector-info-form.html", {
                "request": request,
                "today": today,
                "error": "❌ Interview date is required. Please select a date."
            })

        try:
            interview_date = datetime.strptime(collector_request.interviewDate.strip(), "%Y-%m-%d")
            if interview_date > datetime.now():
                return templates.TemplateResponse("/form/collector-info-form.html", {
                    "request": request,
                    "today": today,
                    "error": "❌ Interview date cannot be in the future. Please select a past or current date."
                })
        except ValueError as e:
            print(f"Date parsing error: {str(e)}")  # Debug log
            return templates.TemplateResponse("/form/collector-info-form.html", {
                "request": request,
                "today": today,
                "error": "❌ Invalid interview date format. Please use YYYY-MM-DD format."
            })

        # === Handle "Other" fields ===
        collection_type = collector_request.collectionType
        if collection_type.lower() == "other" and collector_request.otherTypeInput:
            collection_type = collector_request.otherTypeInput.strip()

        collection_medium = collector_request.collectionMedium
        if collection_medium.lower() == "other" and collector_request.otherMediumInput:
            collection_medium = collector_request.otherMediumInput.strip()

        collection_style = collector_request.collectionStyle
        if collection_style.lower() == "other" and collector_request.otherStyleInput:
            collection_style = collector_request.otherStyleInput.strip()

        # === Validate field lengths ===
        if len(collection_type) > 20 or len(collection_medium) > 15 or len(collection_style) > 15:
            return templates.TemplateResponse("/form/collector-info-form.html", {
                "request": request,
                "today": today,
                "error": "❌ Collection Type (max 20) or Medium/Style (max 15) exceeded."
            })

        if len(collector_request.firstName) > 15 or len(collector_request.lastName) > 20:
            return templates.TemplateResponse("/form/collector-info-form.html", {
                "request": request,
                "today": today,
                "error": "❌ First Name (max 15) or Last Name (max 20) exceeded."
            })

        if len(collector_request.interviewerName) > 35:
            return templates.TemplateResponse("/form/collector-info-form.html", {
                "request": request,
                "today": today,
                "error": "❌ Interviewer Name cannot exceed 35 characters."
            })

        if len(collector_request.street) > 50:
            return templates.TemplateResponse("/form/collector-info-form.html", {
                "request": request,
                "today": today,
                "error": "❌ Street address cannot exceed 50 characters."
            })

        # === Validate field formats ===
        if len(collector_request.socialSecurityNumber.replace("-", "")) != 9:
            return templates.TemplateResponse("/form/collector-info-form.html", {
                "request": request,
                "today": today,
                "error": "❌ SSN must be exactly 9 digits."
            })

        # Check if SSN already exists
        existing_collector = db.query(Collector).filter_by(socialsecuritynumber=collector_request.socialSecurityNumber.replace("-", "").strip()).first()
        if existing_collector:
            return templates.TemplateResponse("/form/collector-info-form.html", {
                "request": request,
                "today": today,
                "error": "❌ This Social Security Number is already registered. Please enter a different one."
            })

        if len(collector_request.areaCode) != 3:
            return templates.TemplateResponse("/form/collector-info-form.html", {
                "request": request,
                "today": today,
                "error": "❌ Area Code must be exactly 3 digits."
            })
        if len(collector_request.telephoneNumber) != 7:
            return templates.TemplateResponse("/form/collector-info-form.html", {
                "request": request,
                "today": today,
                "error": "❌ Telephone Number must be exactly 7 digits."
            })
        if len(collector_request.zip) != 5:
            return templates.TemplateResponse("/form/collector-info-form.html", {
                "request": request,
                "today": today,
                "error": "❌ ZIP Code must be exactly 5 digits."
            })

        # === Lookup artistId if needed ===
        collection_artist_id = None
        if collector_request.collectionArtistFirstName or collector_request.collectionArtistLastName:
            artist_name = f"{collector_request.collectionArtistFirstName.strip()} {collector_request.collectionArtistLastName.strip()}"
            artist = db.query(Artist).filter(
                (Artist.firstname + ' ' + Artist.lastname).ilike(artist_name)
            ).first()
            if not artist:
                return templates.TemplateResponse("/form/collector-info-form.html", {
                    "request": request,
                    "today": today,
                    "error": "❌ Artist not found. Leave artist fields blank if not applicable."
                })
            collection_artist_id = artist.artistid

        # === Insert new Collector ===
        new_collector = Collector(
            socialsecuritynumber=collector_request.socialSecurityNumber.replace("-", "").strip(),
            firstname=collector_request.firstName.strip(),
            lastname=collector_request.lastName.strip(),
            interviewdate=interview_date,
            interviewername=collector_request.interviewerName.strip(),
            areacode=collector_request.areaCode.strip(),
            telephonenumber=collector_request.telephoneNumber.strip(),
            street=collector_request.street.strip(),
            zip=collector_request.zip.strip(),
            saleslastyear=collector_request.salesLastYear or 0,
            salesyeartodate=collector_request.salesYearToDate or 0,
            collectionartistid=collection_artist_id,
            collectionmedium=collection_medium.strip(),
            collectionstyle=collection_style.strip(),
            collectiontype=collection_type.strip()
        )

        db.add(new_collector)
        db.commit()

        return templates.TemplateResponse("/form/collector-info-form.html", {
            "request": request,
            "today": today,
            "success": True
        })

    except (IntegrityError, DataError, oracledb.DatabaseError) as e:
        db.rollback()
        error_msg = str(e)
        if "COLLECTOR_SSN_PK" in error_msg:
            return templates.TemplateResponse("/form/collector-info-form.html", {
                "request": request,
                "today": today,
                "error": "❌ This Social Security Number is already registered. Please enter a different one."
            })
        elif "ZIP_FK" in error_msg:
            return templates.TemplateResponse("/form/collector-info-form.html", {
                "request": request,
                "today": today,
                "error": "❌ ZIP code not found. Use a valid ZIP."
            })
        elif "ORA-12899" in error_msg:
            if "SOCIALSECURITYNUMBER" in error_msg:
                return templates.TemplateResponse("/form/collector-info-form.html", {
                    "request": request,
                    "today": today,
                    "error": "❌ SSN must be exactly 9 digits."
                })
            elif "ZIP" in error_msg:
                return templates.TemplateResponse("/form/collector-info-form.html", {
                    "request": request,
                    "today": today,
                    "error": "❌ ZIP must be exactly 5 digits."
                })
            elif "COLLECTIONTYPE" in error_msg:
                return templates.TemplateResponse("/form/collector-info-form.html", {
                    "request": request,
                    "today": today,
                    "error": "❌ Collection Type exceeds 20 characters."
                })
            elif "COLLECTIONMEDIUM" in error_msg:
                return templates.TemplateResponse("/form/collector-info-form.html", {
                    "request": request,
                    "today": today,
                    "error": "❌ Collection Medium exceeds 15 characters."
                })
            elif "COLLECTIONSTYLE" in error_msg:
                return templates.TemplateResponse("/form/collector-info-form.html", {
                    "request": request,
                    "today": today,
                    "error": "❌ Collection Style exceeds 15 characters."
                })
        return templates.TemplateResponse("/form/collector-info-form.html", {
            "request": request,
            "today": today,
            "error": "❌ Database error. Please check your input and try again."
        })

    except Exception as e:
        db.rollback()
        return templates.TemplateResponse("/form/collector-info-form.html", {
            "request": request,
            "today": today,
            "error": f"❌ Unexpected Error: {str(e)}"
        })
    
@router.get('/artwork-form')
async def get_artwork(request: Request): 
    today = datetime.now().strftime('%Y-%m-%d')
    return templates.TemplateResponse("/form/artwork-info-form.html", {"request": request, "today": today})

@router.post('/add-artwork', response_class=HTMLResponse)
async def add_artwork(
    request: Request,
    db: Session = Depends(get_db),
    artwork_request: ArtworkRequest = Depends(ArtworkRequest.as_form)
):
    today = datetime.now().strftime('%Y-%m-%d')
    CURRENT_YEAR = 2025

    try:
        print("Received artwork request:", artwork_request.dict())
        
        # === Asking Price validation ===
        if not artwork_request.dateListed:
            return templates.TemplateResponse("/form/artwork-info-form.html", {
                "request": request,
                "today": today,
                "error": "❌ Date Listed is required."
            })

        if not artwork_request.askingPrice:
            return templates.TemplateResponse("/form/artwork-info-form.html", {
                "request": request,
                "today": today,
                "error": "❌ Asking Price is required."
            })

        try:
            asking_price = float(artwork_request.askingPrice)
            if asking_price <= 0:
                return templates.TemplateResponse("/form/artwork-info-form.html", {
                    "request": request,
                    "today": today,
                    "error": "❌ Asking Price must be greater than 0."
                })
        except ValueError:
            return templates.TemplateResponse("/form/artwork-info-form.html", {
                "request": request,
                "today": today,
                "error": "❌ Asking Price must be a valid number."
            })

        # === Lookup Artist ===
        artist = db.query(Artist).filter(
            (Artist.firstname.ilike(artwork_request.artistFirstName.strip())) &
            (Artist.lastname.ilike(artwork_request.artistLastName.strip()))
        ).first()

        if not artist:
            return templates.TemplateResponse("/form/artwork-info-form.html", {
                "request": request,
                "today": today,
                "error": "❌ Artist not found."
            })

        artist_id = artist.artistid
        print(f"Found artist with ID: {artist_id}")

        # === Handle "Other" fields ===
        work_type = artwork_request.usualType
        if work_type.lower() == "other" and artwork_request.otherType:
            work_type = artwork_request.otherType.strip()

        work_medium = artwork_request.usualMedium
        if work_medium.lower() == "other" and artwork_request.otherMedium:
            work_medium = artwork_request.otherMedium.strip()

        work_style = artwork_request.usualStyle
        if work_style.lower() == "other" and artwork_request.otherStyle:
            work_style = artwork_request.otherStyle.strip()

        # === Validate Year Completed ===
        if not artwork_request.yearCompleted.isdigit() or len(artwork_request.yearCompleted) != 4:
            return templates.TemplateResponse("/form/artwork-info-form.html", {
                "request": request,
                "today": today,
                "error": "❌ Year must be exactly 4 digits."
            })

        year_completed = int(artwork_request.yearCompleted)
        if year_completed > CURRENT_YEAR:
            return templates.TemplateResponse("/form/artwork-info-form.html", {
                "request": request,
                "today": today,
                "error": f"❌ Year cannot be beyond {CURRENT_YEAR}."
            })

        # === Validate Lengths ===
        if len(work_type) > 20 or len(work_medium) > 15 or len(work_style) > 15:
            return templates.TemplateResponse("/form/artwork-info-form.html", {
                "request": request,
                "today": today,
                "error": "❌ Work Type / Medium / Style exceeds length limits."
            })
        if len(artwork_request.title) > 50:
            return templates.TemplateResponse("/form/artwork-info-form.html", {
                "request": request,
                "today": today,
                "error": "❌ Title exceeds 50 characters."
            })
        if len(artwork_request.size) > 15:
            return templates.TemplateResponse("/form/artwork-info-form.html", {
                "request": request,
                "today": today,
                "error": "❌ Size exceeds 15 characters."
            })

        # === Insert Artwork ===
        new_artwork = Artwork(
            artistid=artist_id,
            worktitle=artwork_request.title.strip(),
            askingprice=asking_price,
            datelisted=datetime.strptime(artwork_request.dateListed.strip(), "%Y-%m-%d"),
            datereturned=None,
            dateshown=None,
            status=artwork_request.status.lower(),
            workmedium=work_medium.strip(),
            worksize=artwork_request.size.strip(),
            workstyle=work_style.strip(),
            worktype=work_type.strip(),
            workyearcompleted=artwork_request.yearCompleted.strip(),
            collectorsocialsecuritynumber=artwork_request.ownerSSN.strip() if artwork_request.ownerSSN else None
        )

        print("Creating new artwork:", new_artwork.__dict__)
        db.add(new_artwork)
        db.commit()
        print("Artwork successfully added to database")

        return templates.TemplateResponse("/form/artwork-info-form.html", {
            "request": request,
            "today": today,
            "success": True
        })

    except IntegrityError as e:
        db.rollback()
        error_msg = str(e)
        print("Database integrity error:", error_msg)
        if "ARTWORK_ARTISTID_TITLE_UK" in error_msg:
            return templates.TemplateResponse("/form/artwork-info-form.html", {
                "request": request,
                "today": today,
                "error": "❌ This artist already has an artwork with the same title. Please use a different title."
            })
        return templates.TemplateResponse("/form/artwork-info-form.html", {
            "request": request,
            "today": today,
            "error": "❌ Database error. Please check your input and try again."
        })

    except Exception as e:
        db.rollback()
        print("Unexpected error:", str(e))
        return templates.TemplateResponse("/form/artwork-info-form.html", {
            "request": request,
            "today": today,
            "error": f"❌ Unexpected error: {str(e)}"
        })



    
@router.get('/sale-invoice')
def get_sale_invoice_form(request: Request): 
    today = datetime.now().strftime('%Y-%m-%d')
    return templates.TemplateResponse("/form/invoice-info.html", {
        "request": request,
        "today": today
    })
@router.post("/add-invoice", response_class=HTMLResponse)
async def add_invoice(
    request: Request,
    db: Session = Depends(get_db),
    artwork_sale: ArtworkSaleRequest = Depends(ArtworkSaleRequest.as_form)
):
    try:
        # Step 1: Get form data
        data = artwork_sale.dict()
        print("Received form data:", data)

        # Validate artist name and artwork title for numbers
        if any(char.isdigit() for char in data['artistFirstName']):
            return templates.TemplateResponse("/form/invoice-info.html", {
                "request": request,
                "error": "❌ Artist's first name cannot contain numbers."
            })
        
        if any(char.isdigit() for char in data['artistLastName']):
            return templates.TemplateResponse("/form/invoice-info.html", {
                "request": request,
                "error": "❌ Artist's last name cannot contain numbers."
            })
        
        if any(char.isdigit() for char in data['artworkTitle']):
            return templates.TemplateResponse("/form/invoice-info.html", {
                "request": request,
                "error": "❌ Artwork title cannot contain numbers."
            })

        # Step 2: Lookup Artwork
        artwork = db.query(Artwork).join(Artist).filter(
            Artwork.worktitle.ilike(data['artworkTitle'].strip()),
            Artist.firstname.ilike(data['artistFirstName'].strip()),
            Artist.lastname.ilike(data['artistLastName'].strip())
        ).first()

        if not artwork:
            return templates.TemplateResponse("/form/invoice-info.html", {
                "request": request,
                "error": "❌ Artwork not found. Please verify Title and Artist."
            })

        if artwork.status.lower() == "sold":
            return templates.TemplateResponse("/form/invoice-info.html", {
                "request": request,
                "error": "❌ This artwork is already sold."
            })

        # Step 3: Lookup Buyer
        buyer = db.query(Buyer).filter(
            Buyer.firstname.ilike(data['buyerFirstName'].strip()),
            Buyer.lastname.ilike(data['buyerLastName'].strip()),
            Buyer.street.ilike(data['buyerStreet'].strip()),
            Buyer.zip == data['buyerZip'].strip()
        ).first()

        if not buyer:
            return templates.TemplateResponse("/form/invoice-info.html", {
                "request": request,
                "error": "❌ Buyer not found. Please register buyer first."
            })

        # Step 4: Lookup Salesperson
        salesperson = db.query(Salesperson).filter(
            Salesperson.socialsecuritynumber == data['salespersonSSN'].strip()
        ).first()

        if not salesperson:
            return templates.TemplateResponse("/form/invoice-info.html", {
                "request": request,
                "error": "❌ Salesperson SSN not found. Please check."
            })

        # Step 5: Validate monetary values
        try:
            sale_price = Decimal(data['salePrice']).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            sale_tax = Decimal(data['saleTax']).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            amount_remitted = Decimal(data['amountRemittedToOwner']).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

            if sale_price <= 0 or amount_remitted <= 0:
                raise ValueError("Sale price and amount remitted must be positive.")
        except Exception as e:
            return templates.TemplateResponse("/form/invoice-info.html", {
                "request": request,
                "error": f"❌ Invalid numeric value: {str(e)}"
            })

        # Set sale date to today
        current_date = datetime.now().date()

        # Step 6: Create Sale
        new_sale = Sale(
            artworkid=artwork.artworkid,
            amountremittedtoowner=float(amount_remitted),
            saledate=current_date,
            saleprice=float(sale_price),
            saletax=float(sale_tax),
            buyerid=buyer.buyerid,
            salespersonssn=data['salespersonSSN'].strip()
        )

        db.add(new_sale)
        try:
            db.flush()  # Flush to get generated invoice number if needed immediately
            # Step 7: Update Artwork Status
            artwork.status = "Sold"
            db.commit()
        except Exception as e:
            db.rollback()
            return templates.TemplateResponse("/form/invoice-info.html", {
                "request": request,
                "error": f"❌ Error creating sale: {str(e)}"
            })

        return templates.TemplateResponse("/form/invoice-info.html", {
            "request": request,
            "success": True,
            "message": new_sale.invoicenumber
        })

    except IntegrityError as e:
        db.rollback()
        error_msg = str(e)
        if "SALE_INVOICENUMBER_PK" in error_msg:
            return templates.TemplateResponse("/form/invoice-info.html", {
                "request": request,
                "today": today,
                "error": "❌ There was a problem generating the invoice number. Please try again."
            })
        return templates.TemplateResponse("/form/invoice-info.html", {
            "request": request,
            "today": today,
            "error": "❌ Database error. Please check your input and try again."
        })

    except Exception as e:
        db.rollback()
        print("Unexpected error during sale creation:", str(e))
        return templates.TemplateResponse("/form/invoice-info.html", {
            "request": request,
            "error": f"❌ Unexpected error: {str(e)}"
        })



    
@router.get("/mailing-list-form")
def mailing_list_form(request: Request): 
    today = datetime.now().strftime('%Y-%m-%d')
    return templates.TemplateResponse("/form/mailing-list-form.html", {
        "request": request,
        "today": today
    })

    
@router.post("/add-mailing-list", response_class=HTMLResponse)
async def add_mailing_list(
    request: Request,
    db: Session = Depends(get_db),
    mailing_request: MailingListRequest = Depends(MailingListRequest.as_form)
):
    try:
        preferred_artist_name = (mailing_request.preferredArtistFirstName.strip() + " " + mailing_request.preferredArtistLastName.strip()).strip()

        # === Check for duplicate ===
        existing_customer = db.query(PotentialCustomer).filter(
            PotentialCustomer.firstname.ilike(mailing_request.firstName.strip()),
            PotentialCustomer.lastname.ilike(mailing_request.lastName.strip()),
            PotentialCustomer.street.ilike(mailing_request.street.strip()),
            PotentialCustomer.zip == mailing_request.zip.strip(),
            PotentialCustomer.telephonenumber == mailing_request.telephoneNumber.strip()
        ).first()

        if existing_customer:
            return templates.TemplateResponse("/form/mailing-list-form.html", {
                "request": request,
                "error": "❌ This person is already on the mailing list."
            })

        # === Lookup artist id ===
        preferred_artist_id = None
        if preferred_artist_name:
            artist = db.query(Artist).filter(
                (Artist.firstname + ' ' + Artist.lastname).ilike(preferred_artist_name)
            ).first()
            if artist:
                preferred_artist_id = artist.artistid

        # === Insert new PotentialCustomer ===
        new_customer = PotentialCustomer(
            firstname=mailing_request.firstName.strip(),
            lastname=mailing_request.lastName.strip(),
            areacode=mailing_request.areaCode.strip(),
            telephonenumber=mailing_request.telephoneNumber.strip(),
            street=mailing_request.street.strip(),
            zip=mailing_request.zip.strip(),
            datefilledin=datetime.strptime(mailing_request.signupDate, "%Y-%m-%d"),
            preferredartistid=preferred_artist_id,
            preferredmedium=mailing_request.preferredMedium.strip() if mailing_request.preferredMedium else None,
            preferredstyle=mailing_request.preferredStyle.strip() if mailing_request.preferredStyle else None,
            preferredtype=mailing_request.preferredType.strip() if mailing_request.preferredType else None
        )

        db.add(new_customer)
        db.commit()

        return templates.TemplateResponse("/form/mailing-list-form.html", {
            "request": request,
            "success": True
        })

    except (oracledb.DatabaseError, IntegrityError, DataError) as e:
        db.rollback()
        error_msg = str(e)
        error = "❌ Database Error."

        if "ORA-12899" in error_msg:
            if "ZIP" in error_msg:
                error = "❌ ZIP must be 5 digits."
            elif "AREACODE" in error_msg:
                error = "❌ Area Code must be 3 digits."
            elif "TELEPHONENUMBER" in error_msg:
                error = "❌ Telephone Number must be 7 digits."
            else:
                error = "❌ Some field length is too long."

        return templates.TemplateResponse("/form/mailing-list-form.html", {
            "request": request,
            "error": error
        })

    except Exception as e:
        db.rollback()
        return templates.TemplateResponse("/form/mailing-list-form.html", {
            "request": request,
            "error": f"❌ Unexpected Error: {str(e)}"
        })

@router.get('/find-artwork',response_class=HTMLResponse )
def find_artwork(request: Request):
    return templates.TemplateResponse("/form/find-artwork.html", {"request": request})
@router.post("/get-filter", response_class=HTMLResponse)
async def get_filtered_artworks(
    request: Request,
    artist_firstname: str = Form(...),
    artist_lastname: str = Form(...),
    type: Optional[str] = Form(None),
    otherType: Optional[str] = Form(None),
    medium: Optional[str] = Form(None),
    otherMedium: Optional[str] = Form(None),
    style: Optional[str] = Form(None),
    otherStyle: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    # If all fields are empty, redirect back to the form
    if not any([artist_firstname, artist_lastname, type, otherType, medium, otherMedium, style, otherStyle]):
        return RedirectResponse(url=request.url_for('form_page_route_name'), status_code=303)

    # Prefer 'Other' inputs if they exist
    final_type = otherType if type == "Other" and otherType else type
    final_medium = otherMedium if medium == "Other" and otherMedium else medium
    final_style = otherStyle if style == "Other" and otherStyle else style

    query = db.query(Artwork).join(Artist)
    query = query.filter(Artwork.status == "for sale")

    # Apply artist name filters
    query = query.filter(
        Artist.firstname.ilike(f"%{artist_firstname.strip()}%"),
        Artist.lastname.ilike(f"%{artist_lastname.strip()}%")
    )

    if final_type:
        query = query.filter(Artwork.worktype.ilike(f"%{final_type}%"))
    if final_medium:
        query = query.filter(Artwork.workmedium.ilike(f"%{final_medium}%"))
    if final_style:
        query = query.filter(Artwork.workstyle.ilike(f"%{final_style}%"))

    artworks = query.all()

    if not artworks:
        message = "No artworks found matching your criteria."
        return templates.TemplateResponse("no_data.html", {"request": request, "message": message})

    return templates.TemplateResponse("filtered_artworks.html", {"request": request, "artworks": artworks})


@router.get("/find-artwork-history-form", response_class=HTMLResponse)
async def show_find_artwork_history_form(request: Request):
    return templates.TemplateResponse("find_artwork_history_form.html", {"request": request})


@router.post("/find-artwork-history", response_class=HTMLResponse)
async def find_artwork_history(
    request: Request,
    artist_firstname: str = Form(...),
    artist_lastname: str = Form(...),
    artwork_title: str = Form(...),
    db: Session = Depends(get_db)
):
    # Validate that all required fields are filled
    if not artist_firstname.strip() or not artist_lastname.strip() or not artwork_title.strip():
        return templates.TemplateResponse("find_artwork_history_form.html", {
            "request": request,
            "error": "❌ All fields (Artist First Name, Last Name, and Artwork Title) are required."
        })

    # Clean user input
    artist_firstname_cleaned = artist_firstname.strip().lower()
    artist_lastname_cleaned = artist_lastname.strip().lower()
    artwork_title_cleaned = artwork_title.strip()

    # Trim the database fields
    trimmed_firstname = func.trim(Artist.firstname)
    trimmed_lastname = func.trim(Artist.lastname)

    # Search
    artwork = (
        db.query(Artwork)
        .join(Artist, Artwork.artistid == Artist.artistid)
        .filter(
            Artwork.worktitle.ilike(f"%{artwork_title_cleaned}%"),
            func.lower(trimmed_firstname) == artist_firstname_cleaned,
            func.lower(trimmed_lastname) == artist_lastname_cleaned
        )
        .first()
    )

    # Get shows and sale info anyway (empty if artwork not found)
    shows = []
    sale = None

    if artwork:
        shows = db.query(ShownIn).filter(ShownIn.artworkid == artwork.artworkid).all()
        sale = db.query(Sale).filter(Sale.artworkid == artwork.artworkid).first()

    return templates.TemplateResponse("artwork_history_result.html", {
        "request": request,
        "artwork": artwork,
        "show_history": shows,
        "sale_info": sale,
        "no_data_message": "No matching artwork found." if not artwork else None
    })

@router.get("/buyer-info", response_class=HTMLResponse)
def get_buyer_form(request: Request):
    return templates.TemplateResponse("/form/buyer-info-form.html", {"request": request})

@router.post("/buyer-info", response_class=HTMLResponse)
async def add_buyer(
    request: Request,
    db: Session = Depends(get_db),
    firstname: str = Form(...),
    lastname: str = Form(...),
    street: Optional[str] = Form(None),
    zip: Optional[str] = Form(None),
    areacode: Optional[str] = Form(None),
    telephonenumber: Optional[str] = Form(None),
    purchaseslastyear: Optional[float] = Form(None),
    purchasesyeartodate: Optional[float] = Form(None)
):
    try:
        print("=== Starting buyer registration process ===")
        print("Received buyer request:", {
            "firstname": firstname,
            "lastname": lastname,
            "street": street,
            "zip": zip,
            "areacode": areacode,
            "telephonenumber": telephonenumber,
            "purchaseslastyear": purchaseslastyear,
            "purchasesyeartodate": purchasesyeartodate
        })

        # Validate required fields
        if not firstname or not lastname:
            print("Validation failed: Missing required fields")
            return templates.TemplateResponse("/form/buyer-info-form.html", {
                "request": request,
                "error": "❌ First Name and Last Name are required."
            })

        # Validate field lengths
        if len(firstname) > 15 or len(lastname) > 20:
            print(f"Validation failed: Field length exceeded - First Name: {len(firstname)}, Last Name: {len(lastname)}")
            return templates.TemplateResponse("/form/buyer-info-form.html", {
                "request": request,
                "error": "❌ First Name (max 15) or Last Name (max 20) exceeded."
            })

        if street and len(street) > 50:
            print(f"Validation failed: Street length exceeded - {len(street)}")
            return templates.TemplateResponse("/form/buyer-info-form.html", {
                "request": request,
                "error": "❌ Street address cannot exceed 50 characters."
            })

        # Validate ZIP code format and existence
        if zip:
            if not zip.isdigit() or len(zip) != 5:
                print(f"Validation failed: Invalid ZIP format - {zip}")
                return templates.TemplateResponse("/form/buyer-info-form.html", {
                    "request": request,
                    "error": "❌ ZIP code must be 5 digits."
                })
            
            # Check if ZIP exists in database
            zip_exists = db.query(ZIPS).filter(ZIPS.zip == zip.strip()).first()
            if not zip_exists:
                print(f"Validation failed: ZIP code not found in database - {zip}")
                return templates.TemplateResponse("/form/buyer-info-form.html", {
                    "request": request,
                    "error": "❌ This ZIP code is not in our database. Please enter a valid ZIP code."
                })

        # Validate area code format
        if areacode and not areacode.isdigit() or (areacode and len(areacode) != 3):
            print(f"Validation failed: Invalid area code format - {areacode}")
            return templates.TemplateResponse("/form/buyer-info-form.html", {
                "request": request,
                "error": "❌ Area code must be 3 digits."
            })

        # Validate telephone number format
        if telephonenumber and not telephonenumber.isdigit() or (telephonenumber and len(telephonenumber) != 7):
            print(f"Validation failed: Invalid telephone number format - {telephonenumber}")
            return templates.TemplateResponse("/form/buyer-info-form.html", {
                "request": request,
                "error": "❌ Telephone number must be 7 digits."
            })

        print("All validations passed, checking for duplicate buyer...")

        # Check for duplicate buyer
        existing_buyer = db.query(Buyer).filter(
            Buyer.firstname.ilike(firstname.strip()),
            Buyer.lastname.ilike(lastname.strip()),
            Buyer.street.ilike(street.strip() if street else ''),
            Buyer.zip == zip.strip() if zip else None
        ).first()

        if existing_buyer:
            print("Duplicate buyer found:", existing_buyer.__dict__)
            return templates.TemplateResponse("/form/buyer-info-form.html", {
                "request": request,
                "error": "❌ A buyer with this information already exists."
            })

        print("No duplicate found, creating new buyer...")

        # Create new buyer
        new_buyer = Buyer(
            firstname=firstname.strip(),
            lastname=lastname.strip(),
            street=street.strip() if street else None,
            zip=zip.strip() if zip else None,
            areacode=areacode.strip() if areacode else None,
            telephonenumber=telephonenumber.strip() if telephonenumber else None,
            purchaseslastyear=purchaseslastyear if purchaseslastyear is not None else None,
            purchasesyeartodate=purchasesyeartodate if purchasesyeartodate is not None else None
        )

        print("New buyer object created:", new_buyer.__dict__)
        print("Attempting to add buyer to database...")

        try:
            db.add(new_buyer)
            db.flush()  # This will trigger the sequence
            print("Buyer added to session, committing...")
            db.commit()
            print("Buyer successfully added to database")
        except Exception as db_error:
            print("Database error during commit:", str(db_error))
            db.rollback()
            raise db_error

        return templates.TemplateResponse("/form/buyer-info-form.html", {
            "request": request,
            "success": "✅ Buyer successfully registered!"
        })

    except IntegrityError as e:
        db.rollback()
        error_msg = str(e)
        print("Database integrity error:", error_msg)
        if "BUYER_PK" in error_msg:
            return templates.TemplateResponse("/form/buyer-info-form.html", {
                "request": request,
                "error": "❌ A buyer with this information already exists."
            })
        elif "ORA-01400" in error_msg:
            return templates.TemplateResponse("/form/buyer-info-form.html", {
                "request": request,
                "error": "❌ There was a problem with the buyer ID. Please try again."
            })
        elif "ORA-02291" in error_msg:
            return templates.TemplateResponse("/form/buyer-info-form.html", {
                "request": request,
                "error": "❌ Invalid ZIP code. Please enter a valid ZIP code."
            })
        return templates.TemplateResponse("/form/buyer-info-form.html", {
            "request": request,
            "error": f"❌ Database error: {error_msg}"
        })

    except Exception as e:
        db.rollback()
        error_type = type(e).__name__
        error_msg = str(e)
        print(f"Unexpected error of type {error_type}:", error_msg)
        print("Full error details:", e.__dict__ if hasattr(e, '__dict__') else "No additional details")
        return templates.TemplateResponse("/form/buyer-info-form.html", {
            "request": request,
            "error": f"❌ Error ({error_type}): {error_msg}"
        })