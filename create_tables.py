from sqlalchemy import create_engine, text
from models.user import Base, User
from database.database import SQLALCHEMY_DATABASE_URL

def create_tables():
    # Create engine
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    
    try:
        # Create sequence if it doesn't exist
        with engine.connect() as conn:
            conn.execute(text("""
                BEGIN
                    EXECUTE IMMEDIATE 'CREATE SEQUENCE "JJUMAEV".user_id_seq
                        START WITH 1
                        INCREMENT BY 1
                        NOCACHE
                        NOCYCLE';
                EXCEPTION
                    WHEN OTHERS THEN
                        IF SQLCODE = -955 THEN
                            NULL; -- Sequence already exists
                        ELSE
                            RAISE;
                        END IF;
                END;
            """))
            conn.commit()

        # Create tables
        Base.metadata.create_all(engine)
        print("✅ Tables created successfully!")
        
    except Exception as e:
        print(f"❌ Error creating tables: {str(e)}")
        raise

if __name__ == "__main__":
    create_tables() 