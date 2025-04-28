from database.database import SessionLocal
from models.artwork import Artwork
from models.collector import Collector
from sqlalchemy import text
import random

def update_artwork_collectors():
    db = SessionLocal()
    try:
        # Get all collectors
        collectors = db.query(Collector).all()
        if not collectors:
            print("No collectors found in the database")
            return

        # Get all artworks
        artworks = db.query(Artwork).all()
        if not artworks:
            print("No artworks found in the database")
            return

        # Assign collectors to artworks
        for artwork in artworks:
            # Skip artworks that are already sold
            if artwork.status and artwork.status.lower() == 'sold':
                continue

            # Randomly assign a collector
            collector = random.choice(collectors)
            
            # Update the artwork
            db.execute(
                text("UPDATE JJUMAEV.ARTWORK SET collectorsocialsecuritynumber = :collector_id WHERE artworkid = :artwork_id"),
                {"collector_id": collector.socialsecuritynumber, "artwork_id": artwork.artworkid}
            )

            # Standardize status
            if artwork.status:
                status = artwork.status.lower()
                if status == 'sold':
                    new_status = 'Sold'
                elif status == 'returned':
                    new_status = 'Returned'
                elif status == 'for sale':
                    new_status = 'For Sale'
                else:
                    new_status = 'For Sale'  # Default status
                
                db.execute(
                    text("UPDATE JJUMAEV.ARTWORK SET status = :status WHERE artworkid = :artwork_id"),
                    {"status": new_status, "artwork_id": artwork.artworkid}
                )

        db.commit()
        print("Successfully updated artwork collectors and statuses")
    except Exception as e:
        print(f"Error updating artwork collectors: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    update_artwork_collectors() 