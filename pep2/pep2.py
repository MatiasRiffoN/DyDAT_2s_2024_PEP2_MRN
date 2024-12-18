import psycopg2
import os
import json
import geopandas as gpd
from sqlalchemy import create_engine

### Funciones ###

# Función utilizada para exportar un GeoDataFrame a una tabla de PostgreSQL #
def export_to_postgis(gdf, table_name, schema="entrada"):
    try:
        gdf.to_postgis(table_name, engine, schema=schema, if_exists="replace", index=False)
        print(f"Tabla '{table_name}' creada exitosamente en el esquema '{schema}'")
    except Exception as e:
        print(f"Error al exportar los datos a PostgreSQL: {e}")

# Función utilizada para cargar datos desde una Geodatabase #

def datos_gdb(gdb_path, feature_class):
    try:
        if not os.path.exists(gdb_path):
            print(f"No se encontró la Geodatabase: {gdb_path}")
            return None
        gdf = gpd.read_file(gdb_path, layer=feature_class)
        print(f"Datos de '{feature_class}' cargados exitosamente desde la Geodatabase")
        return gdf
    except Exception as e:
        print(f"Error al cargar la Geodatabase: {e}")
        return None

# Función utilizada para cargar la configuración de la conexión con la database #

def load_config(config_path):
    try:
        with open(config_path, "r") as config_file:
            config = json.load(config_file)
            return config["database"]
    except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
        print(f"Error al leer el archivo de configuración: {e}")
        exit()

# Función utilizada para crear una conexión con la base de datos y crear esquemas #

def create_connection(db_config):
    try:
        # Conexión con SQLAlchemy para GeoPandas
        engine = create_engine(
            f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['db']}"
        )
        
        # Conexión con psycopg2
        conn = psycopg2.connect(
            dbname=db_config["db"],
            user=db_config["user"],
            password=db_config["password"],
            host=db_config["host"],
            port=db_config["port"]
        )
        cur = conn.cursor()
        cur.execute("CREATE SCHEMA IF NOT EXISTS entrada;")
        cur.execute("CREATE SCHEMA IF NOT EXISTS resultados;")
        conn.commit()
        print("Conexión y esquemas creados exitosamente")
        return engine, conn, cur
    except psycopg2.OperationalError as e:
        print(f"Error en la conexión con psycopg2: {e}")
        exit()
    except Exception as e:
        print(f"Error general: {e}")
        exit()


# Función utilizada para ejecutar un script SQL #

def execute_sql_script(script_path, conn, cur):
    try:
        with open(script_path, "r") as sql_file:
            sql_script = sql_file.read()
        cur.execute(sql_script)
        conn.commit()
        print("Script SQL ejecutado exitosamente")
    except Exception as e:
        print(f"Error al ejecutar el script SQL: {e}")
        conn.rollback()


#Cargar la configuración de la base de datos
config_path = "./config.json"
db_config = load_config(config_path)
engine, conn, cur = create_connection(db_config)

#Cargar datos desde la GDB
gdb_path = r"./pep_2.gdb"

predios_gdb = datos_gdb(gdb_path, "predios")
if predios_gdb is None:
    cur.close()
    conn.close()
    exit()

supermercados_gdb = datos_gdb(gdb_path, "supermercados")
if supermercados_gdb is None:
    cur.close()
    conn.close()
    exit()

manzanas_gdb = datos_gdb(gdb_path, "manzana")
if manzanas_gdb is None:
    cur.close()
    conn.close()
    exit()

zonas_censales_gdb = datos_gdb(gdb_path, "zona_censal")
if zonas_censales_gdb is None:
    cur.close()
    conn.close()
    exit()

# Transformar la proyección de los datos a SRID 32718
predios_gdb = predios_gdb.to_crs(epsg=32718)
manzanas_gdb = manzanas_gdb.to_crs(epsg=32718)
zonas_censales_gdb = zonas_censales_gdb.to_crs(epsg=32718)
supermercados_gdb = supermercados_gdb.to_crs(epsg=32718)

# Exportar los datos a PostgreSQL
export_to_postgis(predios_gdb, "predios")
export_to_postgis(supermercados_gdb, "supermercados")
export_to_postgis(manzanas_gdb, "manzanas")
export_to_postgis(zonas_censales_gdb, "zonas_censales")

# Ruta al script SQL
sql_script_path = "./pep.sql"

# Ejecutar el script SQL y guardar los resultados en el esquema 'resultados'
execute_sql_script(sql_script_path, conn, cur)

# Cerrar el cursor y la conexión
cur.close()
conn.close()
