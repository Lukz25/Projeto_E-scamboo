from flask import Blueprint, request, jsonify
from arquivoClasses.classes import Autor, Titulo

bp_autor = Blueprint("/autor/", "__name__", url_prefix= "/autor")

def autor_para_json(autor: Autor) -> dict:
    return {
        "id": autor.id,
        "nome": autor.nome,
        "obras": [titulo.nome for titulo in autor.obras],
    }

@bp_autor.route("/", methods=['GET'])
def listar():
    return jsonify([autor_para_json(autor) for autor in Autor.listar()]), 200

@bp_autor.route("/<int:id>", methods=['GET'])
def buscar(id):
    autor = Autor.buscar(id)
    if autor is None:
        return jsonify({'erro': 'Autor não encontrado.'}), 404
    return jsonify(autor_para_json(autor)), 200

@bp_autor.route("/", methods=['POST'])
def cadastrar():
    corpo = request.get_json()
    nome = corpo.get('nome')
    if not nome:
        return jsonify({'erro': 'Informe o nome do autor.'}), 400

    autor = Autor(None, nome)
    try:
        autor.salvar()
    except ValueError as erro:
        return jsonify({'erro': str(erro)}), 400
    return jsonify(autor_para_json(autor)), 201

@bp_autor.route("/<int:id>", methods=['PUT'])
def atualizar(id):
    autor = Autor.buscar(id)
    if autor is None:
        return jsonify({'erro': 'Autor não encontrado.'}), 404

    corpo = request.get_json()
    nome = corpo.get('nome')
    if not nome:
        return jsonify({'erro': 'Informe o nome do autor.'}), 400

    autor.nome = nome
    try:
        autor.salvar()
    except ValueError as erro:
        return jsonify({'erro': str(erro)}), 400
    return jsonify(autor_para_json(autor)), 200

@bp_autor.route("/<int:id>", methods=['DELETE'])
def remover(id):
    autor = Autor.buscar(id)
    if autor is None:
        return jsonify({'erro': 'Autor não encontrado.'}), 404

    try:
        autor.remover()
    except ValueError as erro:
        return jsonify({'erro': str(erro)}), 400
    return jsonify({'mensagem': 'Autor removido.'}), 200

@bp_autor.route("/<int:id>/obras/<int:titulo_id>", methods=['POST'])
def adicionar_obra(id, titulo_id):
    autor = Autor.buscar(id)
    titulo = Titulo.buscar(titulo_id)
    if autor is None or titulo is None:
        return jsonify({'erro': 'Autor ou título não encontrado.'}), 404

    autor.adicionar_obra(titulo)
    titulo.salvar()
    return jsonify(autor_para_json(autor)), 200

@bp_autor.route("/<int:id>/obras/<int:titulo_id>", methods=['DELETE'])
def remover_obra(id, titulo_id):
    autor = Autor.buscar(id)
    titulo = Titulo.buscar(titulo_id)
    if autor is None or titulo is None:
        return jsonify({'erro': 'Autor ou título não encontrado.'}), 404

    autor.remover_obra(titulo)
    titulo.salvar()
    return jsonify(autor_para_json(autor)), 200
