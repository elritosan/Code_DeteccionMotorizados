DROP TRIGGER IF EXISTS insert_d_motorizado ON dsa.motorizados;
DROP FUNCTION IF EXISTS edw.trg_insert_d_motorizado;

DROP TRIGGER IF EXISTS call_sp_d_tiempo_calendario ON dsa.motorizados;
DROP FUNCTION IF EXISTS edw.trg_call_sp_d_tiempo_calendario;

DROP TRIGGER IF EXISTS insert_h_moto ON dsa.motorizados;
DROP FUNCTION IF EXISTS edw.trg_insert_h_moto;


-- Trigger 1: Insertar en edw.d_motorizado cuando se agregue un nuevo registro en dsa.motorizados
CREATE OR REPLACE FUNCTION edw.trg_insert_d_motorizado()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO edw.d_motorizado (cod_motorizado, placa)
    VALUES (NEW.id_motorizado, NEW.placa);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER insert_d_motorizado
AFTER INSERT ON dsa.motorizados
FOR EACH ROW
EXECUTE FUNCTION edw.trg_insert_d_motorizado();

-- Trigger 2: Llamar al procedimiento almacenado al iniciar un nuevo año
CREATE OR REPLACE FUNCTION edw.trg_call_sp_d_tiempo_calendario()
RETURNS TRIGGER AS $$
DECLARE
    last_year TEXT;
    new_year TEXT;
BEGIN
    -- Obtener el año del nuevo registro
    new_year := TO_CHAR(NEW.fecha, 'YYYY');

    -- Obtener el último año registrado en la tabla
    SELECT TO_CHAR(MAX(fecha), 'YYYY') INTO last_year FROM dsa.motorizados;

    -- Ejecutar el procedimiento solo si el nuevo año es diferente del último año registrado
    IF last_year IS NULL OR new_year <> last_year THEN
        EXECUTE format('CALL edw.sp_d_tiempo_calendario(''%s-01-01'', ''%s-12-31'')', new_year, new_year);
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER call_sp_d_tiempo_calendario
AFTER INSERT ON dsa.motorizados
FOR EACH ROW
EXECUTE FUNCTION edw.trg_call_sp_d_tiempo_calendario();

-- Trigger 3: Insertar en edw.h_moto después del primer trigger
CREATE OR REPLACE FUNCTION edw.trg_insert_h_moto()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO edw.h_moto (id_motorizado, id_tiempo, cant_personas, cant_cascos)
    SELECT 
        DM.id_motorizado,
        TO_NUMBER(TO_CHAR(NEW.fecha, 'YYYYMMDD'), '99999999') AS id_tiempo,
        NEW.personas,
        NEW.cascos
    FROM edw.d_motorizado DM
    WHERE DM.cod_motorizado = NEW.id_motorizado;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER insert_h_moto
AFTER INSERT ON dsa.motorizados
FOR EACH ROW
EXECUTE FUNCTION edw.trg_insert_h_moto();