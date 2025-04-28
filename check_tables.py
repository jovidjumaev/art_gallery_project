from sqlalchemy import create_engine, text
from database.database import SQLALCHEMY_DATABASE_URL

def check_tables():
    # Create engine
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    
    try:
        with engine.connect() as conn:
            # Check if USERS table exists
            result = conn.execute(text("""
                SELECT table_name 
                FROM all_tables 
                WHERE owner = 'JJUMAEV' 
                AND table_name = 'USERS'
            """))
            users_exists = result.fetchone()
            
            if users_exists:
                print("✅ USERS table exists")
                
                # Get table structure
                result = conn.execute(text("""
                    SELECT column_name, data_type, nullable
                    FROM all_tab_columns
                    WHERE owner = 'JJUMAEV'
                    AND table_name = 'USERS'
                    ORDER BY column_id
                """))
                
                print("\nTable Structure:")
                print("----------------")
                for row in result:
                    print(f"Column: {row[0]}, Type: {row[1]}, Nullable: {row[2]}")
                
                # Check for triggers
                result = conn.execute(text("""
                    SELECT trigger_name, trigger_type, triggering_event
                    FROM all_triggers
                    WHERE owner = 'JJUMAEV'
                    AND table_name = 'USERS'
                """))
                
                print("\nTriggers:")
                print("---------")
                for row in result:
                    print(f"Trigger: {row[0]}, Type: {row[1]}, Event: {row[2]}")
            else:
                print("❌ USERS table does not exist")
                
    except Exception as e:
        print(f"❌ Error checking tables: {str(e)}")
        raise

if __name__ == "__main__":
    check_tables() 