from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models.zips import ZIPS
from pydantic import BaseModel
from database.database import SessionLocal

router = APIRouter()

class ZipCode(BaseModel):
    zip: str
    city: str
    state: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/api/zip/{zip_code}")
async def get_zip_info(zip_code: str, db: Session = Depends(get_db)):
    try:
        zip_info = db.query(ZIPS).filter_by(zip=zip_code).first()
        if zip_info:
            return {
                "city": zip_info.city,
                "state": zip_info.state
            }
        return {"city": None, "state": None}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/zip/add")
async def add_zip(zip_data: ZipCode, db: Session = Depends(get_db)):
    try:
        # Check if ZIP code already exists
        existing_zip = db.query(ZIPS).filter_by(zip=zip_data.zip).first()
        if existing_zip:
            raise HTTPException(status_code=400, detail="ZIP code already exists")
        
        # Create new ZIP code entry
        new_zip = ZIPS(
            zip=zip_data.zip,
            city=zip_data.city,
            state=zip_data.state
        )
        
        db.add(new_zip)
        db.commit()
        db.refresh(new_zip)  # Refresh to ensure the object is properly loaded
        
        return {
            "message": "ZIP code added successfully",
            "city": new_zip.city,
            "state": new_zip.state
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e)) 