from flask import Flask, request, jsonify, render_template
from couchbase.auth import PasswordAuthenticator
from couchbase.cluster import Cluster
from couchbase.options import ClusterOptions
from datetime import timedelta
import traceback

app = Flask(__name__)

# Configuración de conexión a Couchbase
endpoint = "couchbases://cb.cnoyxu1i19qznxqk.cloud.couchbase.com"
username = "valverde"
password = "Valverde24c#"

cluster = None
collection = None

try:
    auth = PasswordAuthenticator(username, password)
    options = ClusterOptions(auth)
    options.apply_profile("wan_development")
    
    cluster = Cluster(endpoint, options)
    cluster.wait_until_ready(timedelta(seconds=10))
    
    bucket = cluster.bucket("tasks")
    scope = bucket.scope("_default")
    collection = scope.collection("_default")
except Exception as e:
    print("Error al conectar al clúster de Couchbase:")
    traceback.print_exc()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tasks', methods=['GET'])
def get_tasks():
    try:
        tasks = []
        query = cluster.query("SELECT meta().id, title, status FROM `tasks`.`_default`.`_default`")
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

@app.route('/tasks', methods=['POST'])
def add_task():
    task_data = request.get_json()
    task_id = f"task::{task_data['title']}"
    task = {'title': task_data['title'], 'status': 'tasksTodo'}
    try:
        collection.upsert(task_id, task)
        return jsonify({'message': 'Task added successfully', 'id': task_id})
    except Exception as e:
        print("Error al agregar la tarea:", e)
        return jsonify({'error': 'Error al agregar la tarea'}), 500

@app.route('/tasks/<task_id>', methods=['PUT'])
def update_task(task_id):
    task_data = request.get_json()
    try:
        collection.mutate_in(task_id, [("status", task_data['status'])])
        return jsonify({'message': 'Task updated successfully'})
    except Exception as e:
        print("Error al actualizar la tarea:", e)
        return jsonify({'error': 'Error al actualizar la tarea'}), 500

@app.route('/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    try:
        collection.remove(task_id)
        return jsonify({'message': 'Task deleted successfully'})
    except Exception as e:
        print("Error al eliminar la tarea:", e)
        return jsonify({'error': 'Error al eliminar la tarea'}), 404

if __name__ == '__main__':
    app.run(debug=True)
