DROP TABLE IF EXISTS dsa.motorizados;

CREATE TABLE dsa.motorizados (
    id_motorizado SERIAL PRIMARY KEY,
    placa TEXT,
    personas INT,
    cascos INT,
    fecha TIMESTAMP DEFAULT NOW()
);