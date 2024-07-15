-- This query counts the number of all doctors with a specific last name.
SELECT COUNT(*) FROM doctor WHERE last_name_doctor = ?;