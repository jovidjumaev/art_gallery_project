from database.database import SessionLocal
from models.artwork import Artwork
from datetime import date, timedelta
import random
from sqlalchemy import text

def update_artwork_dates():
    db = SessionLocal()
    try:
        # Get all for-sale artworks
        artworks = db.query(Artwork).filter(Artwork.status == 'for sale').all()
        
        # Update dates for half of the artworks to be in the past
        for artwork in artworks[:len(artworks)//2]:
            # Generate a random date between 1 and 12 months ago
            months_ago = random.randint(1, 12)
            past_date = date.today() - timedelta(days=30 * months_ago)
            
            # Update using raw SQL to avoid schema issues
            db.execute(
                text("UPDATE JJUMAEV.ARTWORK SET datelisted = :date WHERE artworkid = :id"),
                {"date": past_date, "id": artwork.artworkid}
            )
        
        db.commit()
        print(f"Updated {len(artworks)//2} artwork dates to be in the past")
    except Exception as e:
        print(f"Error updating dates: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    update_artwork_dates() 