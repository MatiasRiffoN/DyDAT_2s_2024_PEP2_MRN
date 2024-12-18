-- Eliminar las tablas si ya existen
DROP TABLE IF EXISTS resultados.predios_optimos;
DROP TABLE IF EXISTS entrada.permiso_supermercados;

-- Crear tabla de permisos de supermercados
CREATE TABLE entrada.permiso_supermercados (
    zona VARCHAR(10),  -- Zona, tipo de dato adecuado dependiendo de la longitud de las zonas
    supermercado INT    -- 1 o 0, para indicar si se puede  construir un supermercado en la zona
);

-- Insertar los permisos de supermercados en las zonas censales obtenidos de la documentación del prc de Puerto Varas https://ptovaras.cl/plan-regulador
INSERT INTO entrada.permiso_supermercados (zona, supermercado) VALUES
('T', 1),('T1', 1),('T1a', 0),('H1', 1),('H1a', 1),('H1b', 1),('H1 EMD', 1),('H2', 1),('H3', 1),('H4', 1),('H5', 1),('C', 1),('CMTE', 1),('C EMD', 1),('CC', 1),('P', 1),('M', 1),('MT', 1),('EM', 1),('ES', 1),('E1', 0),('E2', 0),('I', 0),('EC', 0),('PU', 0),('AV', 0),('R2', 0),('R3', 0),('R4', 0),('R5', 0),('R6', 0),('PLAZA', 0);

-- Crear la CTE para las zonas con supermercados, ahora con la columna geometry
WITH zonas_sm AS (
    SELECT DISTINCT z."ZONA", z.geometry  -- Seleccionamos la geometría junto con el identificador de la zona censal
    FROM entrada.zonas_censales z
    JOIN entrada.supermercados s
    ON ST_Intersects(z.geometry, s.geometry)  -- Verifica que los supermercados estén dentro de las zonas censales
)
-- Crear la tabla con los predios fuera de las zonas con supermercados
SELECT p."COD", p."Zona_1", p."Rol", p."Propiedad", p."Tipo", p."Area_m", p.geometry
INTO resultados.predios_optimos  -- Crear la tabla directamente con los resultados
FROM entrada.predios p
LEFT JOIN zonas_sm zs
ON ST_Intersects(p.geometry, zs.geometry)  -- Verifica la relación espacial de los predios con las zonas con supermercados
WHERE zs."ZONA" IS NULL;  -- Filtra aquellos que no están dentro de las zonas con supermercados

-- Eliminar los predios que no tienen permiso para construir supermercados
DELETE FROM resultados.predios_optimos
USING entrada.permiso_supermercados ps
WHERE resultados.predios_optimos."Zona_1" = ps.zona
AND ps.supermercado = 0;

-- Elminar los predios que son de SERVIU, MUNICIPAL, AREA VERDE o EQUIPAMIENTO
DELETE FROM resultados.predios_optimos
WHERE "Propiedad" IN ('SERVIU', 'MUNICIPAL')
OR "Tipo" IN ('AREA VERDE', 'EQUIPAMIENTO');

-- Eliminar los predios con un area menor a 1000 metros cuadrados
DELETE FROM resultados.predios_optimos
WHERE "Area_m" < 1000;

-- Eliminar los registros de predios que se encuentren dentro del buffer de 700 metros de los supermercados
DELETE FROM resultados.predios_optimos
WHERE EXISTS (
    SELECT 1
    FROM entrada.supermercados s
    WHERE ST_DWithin(resultados.predios_optimos.geometry, s.geometry, 700)
);

-- Campo de cantidad de habitantes en 500 metros
ALTER TABLE resultados.predios_optimos
ADD COLUMN total_habitantes INT;

-- Actualizar el campo total_habitantes con el total de habitantes dentro del buffer
WITH predios_buffer AS (
    SELECT p."COD",  -- Identificador del predio
            ST_Buffer(ST_Centroid(p.geometry), 500) AS buffer_geom
    FROM resultados.predios_optimos p
)

UPDATE resultados.predios_optimos psc
SET total_habitantes = (
    SELECT COALESCE(SUM(m."TOTAL_PERS"), 0)  -- Sumar habitantes en el buffer, y asignar 0 si no hay intersección
    FROM entrada.manzanas m
    JOIN predios_buffer pb
    ON ST_Intersects(pb.buffer_geom, m.geometry)  -- Verifica la intersección entre el buffer y la manzana
    WHERE psc."COD" = pb."COD"  -- Relacionar los registros por COD
);

-- Eliminar los predios con menos de 10000 habitantes en 500 metros
DELETE FROM resultados.predios_optimos
WHERE "total_habitantes" < 10000;
