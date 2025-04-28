import oracledb
from database.database import username as db_username, password, host, port, service_name
from datetime import datetime

def test_login_trigger():
    try:
        # Connect using proper Oracle connection string
        dsn = f"""(DESCRIPTION=
                    (ADDRESS=(PROTOCOL=TCP)(HOST={host})(PORT={port}))
                    (CONNECT_DATA=(SERVICE_NAME={service_name})))"""
        
        connection = oracledb.connect(
            user=db_username,
            password=password,
            dsn=dsn
        )
        
        cursor = connection.cursor()
        
        # Get first user's details before update
        cursor.execute('SELECT USER_ID, USERNAME, LAST_LOGIN FROM "JJUMAEV"."USERS" WHERE ROWNUM = 1')
        user_before = cursor.fetchone()
        
        if user_before:
            user_id, user_name, last_login_before = user_before
            print(f"\nBefore update:")
            print(f"User ID: {user_id}")
            print(f"Username: {user_name}")
            print(f"Last Login: {last_login_before}")
            
            # Update something trivial about the user to trigger the last login update
            cursor.execute(
                'UPDATE "JJUMAEV"."USERS" SET USERNAME = :username WHERE USER_ID = :user_id',
                {'username': user_name, 'user_id': user_id}
            )
            connection.commit()
            
            # Get user details after update
            cursor.execute('SELECT USER_ID, USERNAME, LAST_LOGIN FROM "JJUMAEV"."USERS" WHERE USER_ID = :user_id',
                         {'user_id': user_id})
            user_after = cursor.fetchone()
            
            if user_after:
                _, _, last_login_after = user_after
                print(f"\nAfter update:")
                print(f"User ID: {user_id}")
                print(f"Username: {user_name}")
                print(f"Last Login: {last_login_after}")
                
                if last_login_after != last_login_before:
                    print("\n✅ Trigger test successful! LAST_LOGIN was automatically updated.")
                else:
                    print("\n❌ Trigger test failed! LAST_LOGIN was not updated.")
        else:
            print("❌ No users found in the database to test with!")
            
    except Exception as e:
        print(f"❌ Error testing trigger: {str(e)}")
        raise
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

if __name__ == "__main__":
    test_login_trigger() 