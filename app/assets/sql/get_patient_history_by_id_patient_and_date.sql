-- Combined query to retrieve patient's history details.
SELECT 
    h.id_history,
    pl.id_prescription,
    p.name_pattern,
    f.name_field, 
    d.last_name_doctor AS planning_doctor_last_name,
    h.date_entrance, 
    h.date_release
FROM 
    history AS h
    INNER JOIN pattern AS p ON p.id_pattern = h.id_pattern
    INNER JOIN field AS f ON f.id_field = h.id_field
    INNER JOIN planning AS pl ON pl.id_history = h.id_history
    INNER JOIN doctor AS d ON d.id_doctor = pl.id_confirmed_doctor
WHERE 
    h.id_patient = ? 
    AND ? BETWEEN h.date_entrance AND h.date_release;
