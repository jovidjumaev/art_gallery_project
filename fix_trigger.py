from sqlalchemy import create_engine, text
from database.database import SQLALCHEMY_DATABASE_URL

def fix_trigger():
    # Create engine
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    
    try:
        with engine.connect() as conn:
            # Drop the existing trigger
            conn.execute(text("""
                DROP TRIGGER "JJUMAEV".USERS_BEFORE_INSERT
            """))
            
            # Create the sequence if it doesn't exist
            conn.execute(text("""
                BEGIN
                    EXECUTE IMMEDIATE 'CREATE SEQUENCE "JJUMAEV".USER_ID_SEQ
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
            
            # Create the new trigger
            conn.execute(text("""
                CREATE OR REPLACE TRIGGER "JJUMAEV".USERS_BEFORE_INSERT
                BEFORE INSERT ON "JJUMAEV".USERS
                FOR EACH ROW
                BEGIN
                    IF :NEW.user_id IS NULL THEN
                        SELECT "JJUMAEV".USER_ID_SEQ.NEXTVAL INTO :NEW.user_id FROM dual;
                    END IF;
                END;
            """))
            
            conn.commit()
            print("✅ Trigger fixed successfully!")
            
    except Exception as e:
        print(f"❌ Error fixing trigger: {str(e)}")
        raise

if __name__ == "__main__":
    fix_trigger() 