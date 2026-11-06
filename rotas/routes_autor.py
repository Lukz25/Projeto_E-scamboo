from flask import Blueprint, request, jsonify
from arquivoClasses.classes import Autor
from dados import dados

bp_autor = Blueprint("/autor/", "__name__", url_prefix= "/autor")

def autor_para_json(autor: Autor) -> dict:
    return {
        "id": autor.id,
        "nome": autor.nome,
        "obras": [titulo.nome for titulo in autor.obras],
    }

@bp_autor.route("/", methods=['GET'])
def listar():
    return jsonify([autor_para_json(autor) for autor in dados.autores.values()]), 200

@bp_autor.route("/<int:id>", methods=['GET'])
def buscar(id):
    autor = dados.autores.get(id)
    if autor is None:
        return jsonify({'erro': 'Autor não encontrado.'}), 404
    return jsonify(autor_para_json(autor)), 200

@bp_autor.route("/", methods=['POST'])
def cadastrar():
    corpo = request.get_json()
    nome = corpo.get('nome')
    if not nome:
        return jsonify({'erro': 'Informe o nome do autor.'}), 400

    novo_id = max(dados.autores, default=0) + 1
    autor = Autor(novo_id, nome)
    dados.autores[novo_id] = autor
    return jsonify(autor_para_json(autor)), 201

@bp_autor.route("/<int:id>", methods=['PUT'])
def atualizar(id):
    autor = dados.autores.get(id)
    if autor is None:
        return jsonify({'erro': 'Autor não encontrado.'}), 404

    corpo = request.get_json()
    nome = corpo.get('nome')
    if not nome:
        return jsonify({'erro': 'Informe o nome do autor.'}), 400

    autor.nome = nome
    return jsonify(autor_para_json(autor)), 200

@bp_autor.route("/<int:id>", methods=['DELETE'])
def remover(id):
    autor = dados.autores.get(id)
    if autor is None:
        return jsonify({'erro': 'Autor não encontrado.'}), 404
    if autor.obras:
        return jsonify({'erro': 'Autor possui obras cadastradas.'}), 400

    del dados.autores[id]
    return jsonify({'mensagem': 'Autor removido.'}), 200