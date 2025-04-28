import oracledb
from database.database import username, password, host, port, service_name

def create_login_trigger():
    try:
        # Connect using proper Oracle connection string
        dsn = f"""(DESCRIPTION=
                    (ADDRESS=(PROTOCOL=TCP)(HOST={host})(PORT={port}))
                    (CONNECT_DATA=(SERVICE_NAME={service_name})))"""
        
        connection = oracledb.connect(
            user=username,
            password=password,
            dsn=dsn
        )
        
        cursor = connection.cursor()
        
        # Drop existing trigger if it exists
        try:
            cursor.execute('DROP TRIGGER "JJUMAEV"."UPDATE_LAST_LOGIN"')
        except:
            pass  # Ignore if trigger doesn't exist
            
        # Create the trigger
        trigger_sql = """
        CREATE TRIGGER "JJUMAEV"."UPDATE_LAST_LOGIN"
        BEFORE UPDATE ON "JJUMAEV"."USERS"
        FOR EACH ROW
        BEGIN
          :new.LAST_LOGIN := SYSTIMESTAMP;
        END;
        """
        
        cursor.execute(trigger_sql)
        connection.commit()
        print("✅ Last login trigger created successfully!")
        
    except Exception as e:
        print(f"❌ Error creating trigger: {str(e)}")
        raise
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

if __name__ == "__main__":
    create_login_trigger() 