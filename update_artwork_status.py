from database.database import SessionLocal
from sqlalchemy import text

def update_artwork_status():
    db = SessionLocal()
    try:
        # Update artworks with None status to For Sale
        db.execute(
            text("UPDATE JJUMAEV.ARTWORK SET status = 'For Sale' WHERE status IS NULL")
        )
        db.commit()
        print("Successfully updated artwork statuses")
    except Exception as e:
        print(f"Error updating artwork statuses: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    update_artwork_status() 