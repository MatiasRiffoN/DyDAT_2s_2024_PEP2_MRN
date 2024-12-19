![image](https://github.com/user-attachments/assets/4ff72efb-ea9b-45a5-bd43-cd7274127b7e)

<div align="center">
  <h1>Diseño y Desarrollo de Aplicaciones Territoriales - PEP 2 - Matías Riffo Núñez</h1>
</div>

<div align="center">
  <img width="200" src="https://upload.wikimedia.org/wikipedia/commons/d/d9/Usach_P1.png" alt="logo Usach">
</div>

<div align="center">
  <h3>Universidad de Santiago de Chile</h3>
  <h3>Facultad de Ingeniería</h3>
  <h3>Departamento de Ingeniería Geoespacial y Ambiental</h3>
</div>

<h1>
  <h2 align="center">Manual de Usuario</h2>
</h1>

<ul>
    <li>Comuna escogida: Puerto Varas</li>
    <li>Servicio elegido: Supermercados</li>
</ul>

<h3>Diccionario</h3>

<p>Dentro del script se utilizan 4 feature class pertenecientes a pep2.gdb:</p>

**`supermercados:`** Feature class del tipo point, contiene puntos de ubicaciones de supermercados en Puerto Varas obtenidos de OpenStreetMap y contrastados con Google Maps. Campos Utilizados: **"name"** contiene registros del nombre del supermercado.

**`zona_censal:`** Feature class del tipo polygon, contiene datos referentes a las zonas censales de Puerto Varas. Campos Utilizados: **"ZONA"** indica cual es el numero de la zona censal respectiva.

**`manzana:`** Feature class del tipo polygon, contiene datos censales a nivel manzana de Puerto Varas. Campos Utilizados: **"TOTAL_PERS"** indica la cantidad de personas que habitan en esa manzana.

**`predios:`** Feature class del tipo polygon, contiene los datos referentes al plan regulador comunal de Puerto Varas del año 2022 Campos Utilizados:

**"Rol"** Indica el rol predial;

**"Propiedad"** Indica el propietario del predio: PRIVADO, MUNICIPAL, ARZOBISPADO, RESERVA PROPIETARIO o SERVIU.

**"Tipo"** Indica el tipo de uso que tiene el predio: AREA VERDE, EQUIPAMIENTO, PRIVADO Y RESERVA MUNICIP.

**"Area_m"** Indica el área del predio en metros cuadrados.

**"COD"** Indica el codigo del predio o de un conjunto de predios.

**"Zona_1"** Indica el tipo de zona del predio según la ordenanza detallada en el PRC.

Dentro del script de sql se ingresa una tabla llamda permiso_supermercado la cual contiene información de si esta permitido o no construir un supermercado en cada zona del PRC según la ordenanza establecida, tiene valor 1 si está permitido y valor 0 si no.

El resultado obtenido se almacena en la tabla llamada **`predios_optimos`** esta contiene registros de los predios ideales para la construcción de supermercados en la zona, en donde se considera: Existencia de supermercado dentro de la misma zona censal, Tamaño en metros cuadrados del predio, Ordenanza del PRC, Cercania de 700 metros de otro supermercado, Cobertura en 500 metros de la población según las manzanas.

<h3>Pasos</h3>


1. Preparar una carpeta que contenga: requirements.txt, pep2.gdb, script pep2.py, script pep.sql y config.json</li>
2. Verificar que la geodatabase contenga:
      <ul>
        <li>manzanas</li>
        <li>predios</li>
        <li>zonas_censales</li>
        <li>supermercados</li>
      </ul>
3. Utilizar un Gestor de base de datos (recomendable PostgreSQL y pgADMIN4) con la extensión PostGIS y crear una database llamada pep2
4. Crear un entorno virtual e instalar los paquetes de la siguiente forma:
   ```bash
   pip install -r"requeriments.txt"
   ```

5. Ingresar sus datos de servidor SQL en config.json
   ```bash
   {
    "database": {
        "db_type": "postgresql",
        "db": "pep2",
        "schema": "entrada",
        "host": "localhost",
        "port": 5432,
        "user": "postgres",
        "password": "postgres"
        }
   }
   ```  
   
7. Ejecutar pep2.py
