-- This query retrieves prescription and medication details for a specific prescription ID 
-- from the medication, drug, dosage, prescription, and label tables.
SELECT 
    l.title_label,
    p.date_prescription, 
    p.date_start_prescription, 
    p.date_end_prescription, 
    p.description,
    m.id_medication,
    dr.name_drug,
    do.quantity_dosage
FROM medication AS m
INNER JOIN drug AS dr ON dr.id_drug = m.id_drug
INNER JOIN dosage AS do ON do.id_dosage = m.id_dosage
INNER JOIN prescription AS p ON p.id_prescription = m.id_prescription
INNER JOIN label AS l ON l.id_label = p.id_label
WHERE m.id_prescription = ?;