from flask_restx import Resource, Namespace, fields
from flask import request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

api = Namespace('Restaurante', description='Restaurante APP API')

# MongoDB connection
mongo_client = MongoClient('mongodb://localhost:27017/')

db = mongo_client['restaurante']

model_usuario = api.model('Usuario', {
    'usuario': fields.String,
    'senha': fields.String
})

# POST method to create a new user

# Define a rota para criar um novo usuário
@api.route('/criar_usuario')
# Classe para criar um novo usuário
class CriarUsuario(Resource):
    # Define o modelo de dados esperado
    @api.expect(model_usuario)
    # Define as respostas possíveis
    @api.response(201, 'Usuário criado com sucesso')
    @api.response(400, 'Erro ao criar usuário')
    # Define a documentação da rota
    @api.doc('Cria um novo usuário e retorna o ID do usuário criado')
    # Método POST para criar um novo usuário
    def post(self):
        # Recebe os dados enviados no corpo da requisição em formato JSON/Dict
        data = request.json
        # Define o dicionário com os dados do usuário
        usuario = {
            'usuario': data['usuario'],
            'senha': data['senha']
        }

        # Acessa a coleção de usuários
        collection = db['usuarios']

        # Insere o usuário no banco de dados
        result = collection.insert_one(usuario)

        # Retorna o ID do usuário criado e o código 201 de sucesso
        return str(result.inserted_id), 201

# POST method to authenticate a user
@api.route('/autenticar')
class Autenticar(Resource):
    @api.expect(model_usuario)
    @api.response(200, 'Autenticação realizada com sucesso')
    @api.response(401, 'Usuário ou senha inválidos')
    @api.doc('Autentica um usuário')
    def post(self):
        data = request.json
        
        # Verifica se o usuário e senha existem no banco de dados
        collection = db['usuarios']

        usuario = collection.find_one({
            'usuario': data['usuario']
        })

        if usuario and usuario['senha'] == data['senha']:
            return 'Autenticado com sucesso', 200
        else:
            return 'Usuário ou senha inválidos', 401

model_pedido = api.model('Pedido', {
    'mesa': fields.Integer,
    'cozinha': fields.List(fields.String),
    'bar': fields.List(fields.String),
    'status': fields.String
})


# POST method to create a new order
@api.route('/criar_pedido')
class CriarPedido(Resource):
    @api.expect(model_pedido)
    @api.response(201, 'Pedido criado com sucesso')
    @api.doc('Cria um novo pedido e retorna o ID do pedido criado')
    def post(self):
        data = request.json
        pedido = {
            'mesa': data['mesa'],
            'cozinha': data['cozinha'],
            'bar': data['bar'],
            'status': 'pendente'
        }

        collection = db['pedidos']

        result = collection.insert_one(pedido)

        return str(result.inserted_id), 201       

# GET method to list all pending orders
@api.route('/listar_pedidos')
class ListarPedidos(Resource):
    @api.response(200, 'Pedidos listados com sucesso')
    def get(self):
        collection = db['pedidos']

        pedidos = collection.find(
            {'status': 'pendente'},
            {'_id':0, 'mesa':1, 'cozinha':1, 'bar':1, 'status':1}
        )

        pedidos = [p for p in pedidos]

        # print(pedidos)

        return pedidos, 200