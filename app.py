from flask import Flask, request, jsonify, Response 
from flask_pymongo import PyMongo
from bson import json_util
from bson.objectid import ObjectId
import pymongo

app = Flask(__name__)
##app.config["MONGO_URI"] = "mongodb://localhost:27017/grafitisdb"
#mongo = PyMongo(app)

url_mongo_atlas = "mongodb+srv://grafiti:12345@cluster0.qecwv.mongodb.net/grafitidb?retryWrites=true&w=majority"
client = pymongo.MongoClient(url_mongo_atlas)
mongo = client.get_database('grafitis')

########################  Usuario  ########################

@app.route('/usuarios', methods=['GET'])
def get_usuarios():
    usuarios = mongo.db.usuarios.find()
    response = json_util.dumps(usuarios)
    return Response(response, mimetype='application/json')

@app.route('/usuarios/<id>', methods=['GET'])
def get_usuario(id):
    usuario = mongo.db.usuarios.find_one({'_id': ObjectId(id)})
    response = json_util.dumps(usuario)
    return Response(response, mimetype='application/json')

@app.route('/usuarios/<id>', methods=['DELETE'])
def delete_usuario(id):
    mongo.db.usuarios.delete_one({'_id': ObjectId(id)})
    response = {'mensaje': 'Usuario eliminado correctamente'}
    return response

@app.route('/usuarios/<id>', methods=['PUT'])
def update_usuario(id):
    nombre = request.json['nombre']
    direccion = request.json['direccion']
    password = request.json['password']
    email = request.json['email']

    if nombre and direccion and password and email:
        mongo.db.usuarios.update_one({'_id': ObjectId(id)}, {'$set': {
            'nombre': nombre, 
            'email': email, 
            'password': password,
            'direccion': direccion
        }})
        response = jsonify({'mensaje': 'Usuario actualizado correctamente'})
        return response
    else: 
        return not_found()

@app.route('/usuarios', methods=['POST'])
def create_usuario():
    nombre = request.json['nombre']
    password = request.json['password']
    email = request.json['email']
    direccion = request.json['direccion']

    if nombre and password and email and direccion:
        id = mongo.db.usuarios.insert(
            {'nombre': nombre, 'email': email, "password": password, 'direccion': direccion}
        )
        response = {
            'id': str(id),
            'nombre': nombre,
            'email': email,
            'password': password,
            'direccion': direccion
        }
        return response
    else: 
        return not_found()

@app.route('/usuarios/findByNombre/<nombre>', methods=['GET'])
def get_usuario_byNombre(nombre):
    myquery = { "nombre": { '$regex': ".*" + nombre + ".*" } }
    usuario = mongo.db.usuarios.find(myquery)
    response = json_util.dumps(usuario)
    return Response(response, mimetype='application/json')



########################  Grafiti  ########################

@app.route('/grafitis', methods=['GET'])
def get_grafitis():
    grafitis = mongo.db.grafitis.find()
    response = json_util.dumps(grafitis)
    return Response(response, mimetype='application/json')

@app.route('/grafitis/<id>', methods=['GET'])
def get_grafiti(id):
    grafiti = mongo.db.grafitis.find_one({'_id': ObjectId(id)})
    response = json_util.dumps(grafiti)
    return Response(response, mimetype='application/json')

@app.route('/grafitis/<id>', methods=['DELETE'])
def delete_grafiti(id):
    mongo.db.grafitis.delete_one({'_id': ObjectId(id)})
    response = {'mensaje': 'Grafiti eliminado correctamente'}
    return response

@app.route('/grafitis/<id>', methods=['PUT'])
def update_grafiti(id):
    nombre = request.json['nombre']
    fecha = request.json['fecha']
    url = request.json['url']
    autor = request.json['autor']
    direccion = request.json['direccion']
    x = request.json['x']
    y = request.json['y']
    usuario_email = request.json['usuario_email']

    if nombre and direccion and fecha and url and autor and x and y:
        mongo.db.grafitis.update_one({'_id': ObjectId(id)}, {'$set': {
            'nombre': nombre, 
            'url': url, 
            'autor': autor,
            'fecha': fecha,
            'x': x,
            'y': y,
            'direccion': direccion,
            'usuario_email': usuario_email
        }})
        response = jsonify({'mensaje': 'Grafiti actualizado correctamente'})
        return response
    else: 
        return not_found()

@app.route('/grafitis', methods=['POST'])
def create_grafiti():
    nombre = request.json['nombre']
    fecha = request.json['fecha']
    url = request.json['url']
    autor = request.json['autor']
    direccion = request.json['direccion']
    x = request.json['x']
    y = request.json['y']
    usuario_email = request.json['usuario_email']

    if nombre and direccion and fecha and url and autor and x and y and usuario_email:
        id = mongo.db.grafitis.insert({
                'nombre': nombre,
                'fecha': fecha,
                'url': url,
                'autor': autor,
                'x': x,
                'y': y,
                'direccion': direccion,
                'usuario_email': usuario_email
            }
        )
        response = {
            'id': str(id),
            'nombre': nombre,
            'fecha': fecha,
            'url': url,
            'autor': autor,
            'x': x,
            'y': y,
            'direccion': direccion,
            'usuario_email': usuario_email
        }
        return response
    else: 
        return not_found()

@app.route('/grafitis/findByNombre/<nombre>', methods=['GET'])
def get_grafiti_byNombre(nombre):
    myquery = { "nombre": { '$regex': ".*" + nombre + ".*" } }
    grafiti = mongo.db.grafitis.find(myquery)
    response = json_util.dumps(grafiti)
    return Response(response, mimetype='application/json')

@app.route('/grafitis/findByUsuario/<email>', methods=['GET'])
def get_grafiti_byUsuario(email):
    myquery = { "usuario_email": email }
    grafiti = mongo.db.grafitis.find(myquery)
    response = json_util.dumps(grafiti)
    return Response(response, mimetype='application/json')



########################  Comentario  ########################

@app.route('/comentarios', methods=['GET'])
def get_comentarios():
    comentarios = mongo.db.comentarios.find()
    response = json_util.dumps(comentarios)
    return Response(response, mimetype='application/json')

@app.route('/comentarios/<id>', methods=['GET'])
def get_comentario(id):
    comentario = mongo.db.comentarios.find_one({'_id': ObjectId(id)})
    response = json_util.dumps(comentario)
    return Response(response, mimetype='application/json')

@app.route('/comentarios/<id>', methods=['DELETE'])
def delete_comentario(id):
    mongo.db.comentarios.delete_one({'_id': ObjectId(id)})
    response = {'mensaje': 'Comentario eliminado correctamente'}
    return response

@app.route('/comentarios/<id>', methods=['PUT'])
def update_comentario(id):
    contenido = request.json['contenido']
    usuario_nombre = request.json['usuario_nombre']
    grafiti_id = request.json['grafiti_id']

    if contenido and usuario_nombre and grafiti_id:
        mongo.db.comentarios.update_one({'_id': ObjectId(id)}, {'$set': {
            'contenido': contenido, 
            'usuario_nombre': usuario_nombre,
            'grafiti_id': grafiti_id
        }})
        response = jsonify({'mensaje': 'comentario actualizado correctamente'})
        return response
    else: 
        return not_found()

@app.route('/comentarios', methods=['POST'])
def create_comentario():
    contenido = request.json['contenido']
    usuario_nombre = request.json['usuario_nombre']
    grafiti_id = request.json['grafiti_id']

    if contenido and usuario_nombre and grafiti_id:
        id = mongo.db.comentarios.insert(
            {'contenido': contenido, 'usuario_nombre': usuario_nombre, "grafiti_id": grafiti_id}
        )
        response = {
            'id': str(id),
            'contenido': contenido,
            'usuario_nombre': usuario_nombre,
            'grafiti_id': grafiti_id
        }
        return response
    else: 
        return not_found()

@app.route('/comentarios/findByGrafiti/<id>', methods=['GET'])
def get_comentario_byGrafiti(id):
    myquery = { "grafiti_id": id }
    comentario = mongo.db.comentarios.find(myquery)
    response = json_util.dumps(comentario)
    return Response(response, mimetype='application/json')




@app.errorhandler(404)
def not_found(error=None):
    response = jsonify({
        'mensaje': 'Recurso no encontrado',
        'estado': 404
    })
    response.status_code = 404
    return response

if __name__ == "__main__":
    app.run(debug=True)