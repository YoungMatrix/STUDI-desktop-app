-- This query retrieves information from the secretary table with specific email.
SELECT 
    last_name_secretary,
    first_name_secretary
FROM secretary
WHERE email_secretary = ?;