-- Creacion Tabla
create table if not EXISTS price_history(
fecha varchar(30),
id_item integer,
merchant varchar(100),
item varchar(100),
precio varchar(100),
carta varchar(100),
random_options varchar(300),
icono varchar(300),
imagen varchar(300)
);
-- Cargamos el CSV (recordar nunca usar el import wizzard del Workbench, tomaría literalmente meses)
LOAD DATA LOCAL INFILE '/Scrapper Afelheim/db_precios.csv'
INTO TABLE price_history
COLUMNS TERMINATED BY ','
IGNORE 1 LINES;