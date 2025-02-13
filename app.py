from flask import Flask, request, jsonify, render_template
from couchbase.auth import PasswordAuthenticator
from couchbase.cluster import Cluster
from couchbase.options import ClusterOptions
import couchbase.subdocument as SD
from datetime import timedelta
import traceback
import uuid

app = Flask(__name__)

# Configuración de conexión a Couchbase
endpoint = "couchbase://localhost"
username = " "
bucket_name = " "
password = " "

cluster = None
collection = None

try:
    print("Conectarse a Couchbase...")
    cluster = Cluster.connect(
        "couchbase://localhost",
        ClusterOptions(PasswordAuthenticator(username, password))
    )
    print("Conectado a Couchbase. Accediendo al bucket...")
    bucket = cluster.bucket(bucket_name)
    scope = bucket.default_scope()
    collection = bucket.default_collection()
    cluster.wait_until_ready(timedelta(seconds=10))
except Exception as e:
    print("Error al conectar con Couchbase:")
    print(cluster)
    traceback.print_exc()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tasks', methods=['GET'])
def get_tasks():
    try:
        tasks = []
        query = cluster.query("SELECT meta().id, title, status FROM " + bucket_name + ".`_default`.`_default`")
        for row in query:
            tasks.append({
                'id': row['id'],
                'title': row['title'],
                'status': row['status']
            })
        return jsonify(tasks)
    except Exception as e:
        print("Error al obtener las tareas:", e)
        return jsonify({'error': 'Error al obtener las tareas'}), 500

@app.route('/tasks/<task_id>', methods=['GET'])
def get_task(task_id):
    try:
        tasks = []
        query = cluster.query("SELECT meta().id, title, status FROM " + bucket_name + ".`_default`.`_default` WHERE id = '" + task_id + "'") 
        print("Query done")
        for task in query.rows():
            tasks.append({
                'id': task['id'],
                'title': task['title'],
                'status': task['status']
            })
        return jsonify(tasks)
    except Exception as e:
        print("Error al obtener las tareas:", e)
        return jsonify({'error': 'Error al obtener las tareas'}), 500

@app.route('/tasks', methods=['POST'])
def add_task():
    task_data = request.get_json()
    task_id = task_id = str(uuid.uuid4())
    task = {'id': task_id, 'title': task_data['title'], 'status': 'tasksTodo'}
    try:
        collection.upsert(task_id, task)
        return jsonify({'message': 'Tarea creada', 'id': task_id})
    except Exception as e:
        print("Error al agregar la tarea:", e)
        return jsonify({'error': 'Error al agregar la tarea'}), 500

@app.route('/tasks/<task_id>', methods=['PUT'])
def update_task(task_id):
    task_data = request.get_json()
    for key, value in task_data.items():
        try:
            collection.mutate_in(task_id, [SD.upsert(key, value)])
            return jsonify({'message': 'Tarea modificada'})
        except Exception as e:
            print("Error al actualizar la tarea:", e)
            return jsonify({'error': 'Error al actualizar la tarea'}), 500

@app.route('/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    try:
        collection.remove(task_id)
        return jsonify({'message': 'Tarea eliminada'})
    except Exception as e:
        print("Error al eliminar la tarea:", e)
        return jsonify({'error': 'Error al eliminar la tarea'}), 404

if __name__ == '__main__':
    app.run(debug=True)
if __name__ == '__main__':
    app.run(debug=True)
