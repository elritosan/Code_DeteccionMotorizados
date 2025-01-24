DROP TABLE IF EXISTS edw.h_moto;
DROP TABLE IF EXISTS edw.d_tiempo;
DROP TABLE IF EXISTS edw.d_motorizado;

CREATE TABLE edw.d_motorizado (
    id_motorizado       SERIAL PRIMARY KEY   NOT NULL,
    cod_motorizado      INT                  NULL,
    placa               VARCHAR(20)          NULL
);

CREATE TABLE edw.d_tiempo (
   id_tiempo            INT PRIMARY KEY      NOT NULL,
   anio                 INT                  NULL,
   mes_num              INT                  NULL,
   mes_nombre           VARCHAR(10)          NULL,
   sem_num              INT4                 NULL,
   sem_nombre           VARCHAR(15)          NULL,
   dia                  DATE                 NULL
);

CREATE TABLE edw.h_moto (
    id_motorizado       INT                  NOT NULL,
    id_tiempo           INT                  NOT NULL,
    cant_personas       INT                  NOT NULL,
    cant_cascos         INT                  NOT NULL,
    PRIMARY KEY (id_motorizado, id_tiempo),
    FOREIGN KEY (id_motorizado) REFERENCES edw.d_motorizado(id_motorizado),
    FOREIGN KEY (id_tiempo) REFERENCES edw.d_tiempo(id_tiempo)
);