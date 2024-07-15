-- This query retrieves password and salt from the secretary table with specific email.
SELECT 
    password_secretary,
    salt_secretary
FROM secretary
WHERE email_secretary = ?;