# Proyecto-simple-Flask-Valverde-Cano

# Pasos para correr la aplicación

1. **Eliminar el entorno virtual actual** (si existe) y crear uno nuevo:
   ```bash
   rm -rf env 
   python3 -m venv env  
   ```

2. **Activar el entorno virtual**:
   - En Windows:
     ```bash
     env\Scripts\activate
     ```

3. **Instalar las dependencias necesarias**:
   ```bash
    pip install flask
    pip install couchbase
   ```

4. **Configurar las credenciales y conexión de CouchDB**:
   - Abre el archivo `app.py`.
   - Actualiza las variables `endpoint`, `username` y `password` con tus credenciales de CouchDB Capella:
     ```python
     endpoint = "tu_endpoint_de_couchdb"
     username = "tu_usuario"
     password = "tu_contraseña"
     ```

5. **Ejecutar la aplicación Flask**:
   - Inicia el servidor Flask con el siguiente comando:
     ```bash
     flask run
     ```

6. **Abrir la aplicación en el navegador**:
   - Una vez iniciado el servidor, abre tu navegador y accede a `http://127.0.0.1:5000` para ver la aplicación.
---


