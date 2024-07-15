-- This query retrieves patient information based on their history within the specified date and orders the results by descending patient id.
SELECT p.id_patient, p.last_name_patient, p.first_name_patient, p.address_patient, p.email_patient
FROM patient AS p 
INNER JOIN history AS h ON p.id_patient = h.id_patient
WHERE ? BETWEEN h.date_entrance AND h.date_release
ORDER BY p.id_patient DESC;
