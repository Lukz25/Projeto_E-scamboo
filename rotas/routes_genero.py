from flask import Blueprint, request, jsonify
from arquivoClasses.classes import Genero

bp_genero = Blueprint("/genero/", "__name__", url_prefix= "/genero")

def genero_para_json(genero: Genero) -> dict:
    return {
        "id": genero.id,
        "nome": genero.nome,
    }

@bp_genero.route("/", methods=['GET'])
def listar():
    return jsonify([genero_para_json(genero) for genero in Genero.listar()]), 200

@bp_genero.route("/<int:id>", methods=['GET'])
def buscar(id):
    genero = Genero.buscar(id)
    if genero is None:
        return jsonify({'erro': 'Genero não encontrado.'}), 404
    return jsonify(genero_para_json(genero)), 200

@bp_genero.route("/", methods=['POST'])
def cadastrar():
    corpo = request.get_json()
    nome = corpo.get('nome')
    if not nome:
        return jsonify({'erro': 'Informe o nome do genero.'}), 400

    genero = Genero(None, nome)
    try:
        genero.salvar()
    except ValueError as erro:
        return jsonify({'erro': str(erro)}), 400
    return jsonify(genero_para_json(genero)), 201

@bp_genero.route("/<int:id>", methods=['PUT'])
def atualizar(id):
    genero = Genero.buscar(id)
    if genero is None:
        return jsonify({'erro': 'Genero não encontrado.'}), 404

    corpo = request.get_json()
    nome = corpo.get('nome')
    if not nome:
        return jsonify({'erro': 'Informe o nome do genero.'}), 400

    genero.nome = nome
    try:
        genero.salvar()
    except ValueError as erro:
        return jsonify({'erro': str(erro)}), 400
    return jsonify(genero_para_json(genero)), 200

@bp_genero.route("/<int:id>", methods=['DELETE'])
def remover(id):
    genero = Genero.buscar(id)
    if genero is None:
        return jsonify({'erro': 'Genero não encontrado.'}), 404

    try:
        genero.remover()
    except ValueError as erro:
        return jsonify({'erro': str(erro)}), 400
    return jsonify({'mensagem': 'Genero removido.'}), 200
