# Database Triggers Documentation

## 1. USERS_BEFORE_INSERT Trigger

### Purpose
This trigger automatically generates a unique user ID for new users when they are inserted into the USERS table.

### Technical Details
- **Trigger Name**: `USERS_BEFORE_INSERT`
- **Schema**: `JJUMAEV`
- **Table**: `USERS`
- **Timing**: `BEFORE INSERT`
- **Type**: `FOR EACH ROW`

### Functionality
1. The trigger fires before a new row is inserted into the USERS table
2. It checks if the `user_id` field is NULL
3. If NULL, it generates a new ID using the `USER_ID_SEQ` sequence
4. The sequence starts at 1 and increments by 1
5. The generated ID is assigned to the new user's `user_id` field

### Sequence Details
- **Name**: `USER_ID_SEQ`
- **Schema**: `JJUMAEV`
- **Start Value**: 1
- **Increment**: 1
- **Cache**: No
- **Cycle**: No

### Example
```sql
-- When inserting a new user without an ID:
INSERT INTO USERS (username, password_hash, email) 
VALUES ('john_doe', 'hashed_password', 'john@example.com');

-- The trigger automatically assigns the next sequence value to user_id
```

## 2. UPDATE_LAST_LOGIN Trigger

### Purpose
This trigger automatically updates the `LAST_LOGIN` timestamp whenever a user's record is updated in the USERS table.

### Technical Details
- **Trigger Name**: `UPDATE_LAST_LOGIN`
- **Schema**: `JJUMAEV`
- **Table**: `USERS`
- **Timing**: `BEFORE UPDATE`
- **Type**: `FOR EACH ROW`

### Functionality
1. The trigger fires before a row is updated in the USERS table
2. It automatically sets the `LAST_LOGIN` field to the current system timestamp
3. This ensures accurate tracking of when users last logged in

### Example
```sql
-- When updating a user's record:
UPDATE USERS 
SET email = 'new_email@example.com' 
WHERE username = 'john_doe';

-- The trigger automatically updates LAST_LOGIN to the current timestamp
```

## Maintenance Notes

### Recreating Triggers
If you need to recreate these triggers, you can use the following Python scripts:
1. `fix_trigger.py` - Recreates the USERS_BEFORE_INSERT trigger
2. `create_login_trigger.py` - Recreates the UPDATE_LAST_LOGIN trigger

### Best Practices
1. Always test triggers in a development environment first
2. Monitor trigger performance as they can impact database operations
3. Keep track of trigger dependencies when making schema changes
4. Document any modifications to trigger behavior

### Troubleshooting
If triggers are not working as expected:
1. Check if the triggers exist in the database
2. Verify the sequence exists and is working
3. Check for any error messages in the database logs
4. Ensure the user has proper permissions to execute the triggers 