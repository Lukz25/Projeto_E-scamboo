from flask import Blueprint, request, jsonify
from arquivoClasses.classes import Genero
from arquivoClasses.dados import dados

bp_genero = Blueprint("/genero/", "__name__", url_prefix= "/genero")

def genero_para_json(genero: Genero) -> dict:
    return {
        "id": genero.id,
        "nome": genero.nome,
    }

@bp_genero.route("/", methods=['GET'])
def listar():
    return jsonify([genero_para_json(genero) for genero in dados.generos.values()]), 200

@bp_genero.route("/<int:id>", methods=['GET'])
def buscar(id):
    genero = dados.generos.get(id)
    if genero is None:
        return jsonify({'erro': 'Genero não encontrado.'}), 404
    return jsonify(genero_para_json(genero)), 200

@bp_genero.route("/", methods=['POST'])
def cadastrar():
    corpo = request.get_json()
    nome = corpo.get('nome')
    if not nome:
        return jsonify({'erro': 'Informe o nome do genero.'}), 400

    novo_id = max(dados.generos, default=0) + 1
    genero = Genero(novo_id, nome)
    dados.generos[novo_id] = genero
    return jsonify(genero_para_json(genero)), 201

@bp_genero.route("/<int:id>", methods=['PUT'])
def atualizar(id):
    genero = dados.generos.get(id)
    if genero is None:
        return jsonify({'erro': 'Genero não encontrado.'}), 404

    corpo = request.get_json()
    nome = corpo.get('nome')
    if not nome:
        return jsonify({'erro': 'Informe o nome do genero.'}), 400

    genero.nome = nome
    return jsonify(genero_para_json(genero)), 200

@bp_genero.route("/<int:id>", methods=['DELETE'])
def remover(id):
    genero = dados.generos.get(id)
    if genero is None:
        return jsonify({'erro': 'Genero não encontrado.'}), 404

    del dados.generos[id]
    return jsonify({'mensagem': 'Genero removido.'}), 200
