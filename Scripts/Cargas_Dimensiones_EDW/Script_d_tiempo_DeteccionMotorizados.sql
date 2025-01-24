DROP PROCEDURE IF EXISTS edw.sp_d_tiempo_calendario;

CREATE PROCEDURE edw.sp_d_tiempo_calendario(IN fechainicio date, IN fechafin date)
LANGUAGE 'plpgsql'
AS $BODY$
DECLARE
    f1 date;
    f2 date;
BEGIN
    f1 := fechainicio;
    f2 := fechafin;

    WHILE (f1 <= f2) LOOP
        INSERT INTO edw.d_tiempo(
            id_tiempo, anio, sem_num, sem_nombre, mes_num, mes_nombre, dia
        )
        VALUES (
            CAST((to_char(f1, 'YYYYMMDD')) AS integer),
            CAST(EXTRACT(YEAR FROM f1) AS smallint),
            CASE
                WHEN (CAST(EXTRACT(MONTH FROM f1) AS integer)) <= 6 THEN 1 ELSE 2
            END,
            CASE
                WHEN (CAST(EXTRACT(MONTH FROM f1) AS integer)) <= 6 THEN 'Semestre 1' ELSE 'Semestre 2'
            END,
            CAST(EXTRACT(MONTH FROM f1) AS smallint),
            CAST(to_char(f1, 'TMMonth') AS varchar(10)),
            f1
        );
        f1 := f1 + INTERVAL '1 day';
    END LOOP;
END;
$BODY$;

--Posteriormente se puede implementar un Tiger para la carga de datos nuevos datos en la tabla d_tiempo
call edw.sp_d_tiempo_calendario('2025-01-01', '2025-12-31');

--SELECT * FROM edw.d_tiempo;