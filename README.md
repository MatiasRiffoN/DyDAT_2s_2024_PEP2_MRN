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

<h3>Diccionario</h3>

<p>Dentro del script se utilizan 4 feature class pertenecientes a pep2.gdb </p>


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
6. Ejecutar pep2.py





