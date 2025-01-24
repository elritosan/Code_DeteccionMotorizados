SELECT
    DM.id_motorizado as id_motorizado,
    TO_NUMBER(TO_CHAR(M.fecha, 'YYYYMMDD'), '99999999') AS id_tiempo,
    M.personas as cant_personas,
    M.cascos as cant_cascos
FROM
    dsa.motorizados M
JOIN
    edw.d_motorizado DM ON M.id_motorizado = DM.id_motorizado;