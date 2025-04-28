from sqlalchemy import create_engine, text
from database.database import SQLALCHEMY_DATABASE_URL

def check_trigger():
    # Create engine
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    
    try:
        with engine.connect() as conn:
            # Get trigger definition
            result = conn.execute(text("""
                SELECT trigger_body
                FROM all_triggers
                WHERE owner = 'JJUMAEV'
                AND trigger_name = 'USERS_BEFORE_INSERT'
            """))
            
            trigger_body = result.fetchone()
            if trigger_body:
                print("Trigger Definition:")
                print("------------------")
                print(trigger_body[0])
            else:
                print("❌ Trigger not found")
                
    except Exception as e:
        print(f"❌ Error checking trigger: {str(e)}")
        raise

if __name__ == "__main__":
    check_trigger() 