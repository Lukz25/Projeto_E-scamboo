from flask import Blueprint, request, jsonify
from arquivoClasses.classes import Autor, Genero, Titulo
from rotas.routes_usuario import usuario_logado

bp_titulo = Blueprint("/titulo/", "__name__", url_prefix= "/titulo")

def titulo_para_json(titulo: Titulo) -> dict:
    return {
        "id": titulo.id,
        "nome": titulo.nome,
        "dono": titulo.usuario.get_email(),
        "dono_nome": titulo.usuario.nome,
        "autores": [autor.nome for autor in titulo.autores],
        "autores_ids": [autor.id for autor in titulo.autores],
        "generos": [genero.nome for genero in titulo.generos],
        "generos_ids": [genero.id for genero in titulo.generos],
        "data_lancamento": titulo.data_lancamento,
        "estado_conservacao": titulo.estado_conservacao,
        "descricao": titulo.descricao,
    }

def buscar_do_dono(id: int):
    usuario = usuario_logado()
    if usuario is None:
        return None, (jsonify({'erro': 'Faça login primeiro.'}), 401)
    titulo = Titulo.buscar(id)
    if titulo is None:
        return None, (jsonify({'erro': 'Título não encontrado.'}), 404)
    if titulo.usuario != usuario:
        return None, (jsonify({'erro': 'Apenas o dono pode alterar este título.'}), 403)
    return titulo, None

def buscar_lista(classe, ids: list):
    itens = [classe.buscar(id) for id in ids]
    return None if None in itens else itens

@bp_titulo.route("/", methods=['GET'])
def listar():
    titulos = Titulo.listar()

    autor_id = request.args.get('autor', type=int)
    if autor_id is not None:
        autor = Autor.buscar(autor_id)
        titulos = [titulo for titulo in titulos if autor is not None and titulo.possui_autor(autor)]

    genero_id = request.args.get('genero', type=int)
    if genero_id is not None:
        genero = Genero.buscar(genero_id)
        titulos = [titulo for titulo in titulos if genero is not None and titulo.possui_genero(genero)]

    return jsonify([titulo_para_json(titulo) for titulo in titulos]), 200

@bp_titulo.route("/<int:id>", methods=['GET'])
def buscar(id):
    titulo = Titulo.buscar(id)
    if titulo is None:
        return jsonify({'erro': 'Título não encontrado.'}), 404
    return jsonify(titulo_para_json(titulo)), 200

@bp_titulo.route("/", methods=['POST'])
def cadastrar():
    usuario = usuario_logado()
    if usuario is None:
        return jsonify({'erro': 'Faça login primeiro.'}), 401

    corpo = request.get_json()
    nome = corpo.get('nome')
    if not nome:
        return jsonify({'erro': 'Informe o nome do título.'}), 400
    autores = buscar_lista(Autor, corpo.get('autores', []))
    if autores is None:
        return jsonify({'erro': 'Autor não encontrado.'}), 404
    generos = buscar_lista(Genero, corpo.get('generos', []))
    if generos is None:
        return jsonify({'erro': 'Gênero não encontrado.'}), 404

    titulo = Titulo(
        None,
        nome,
        usuario,
        autores,
        generos,
        corpo.get('data_lancamento', ''),
        corpo.get('estado_conservacao', ''),
        corpo.get('descricao', ''),
    )
    titulo.salvar()
    return jsonify(titulo_para_json(titulo)), 201

@bp_titulo.route("/<int:id>", methods=['PUT'])
def atualizar(id):
    titulo, erro = buscar_do_dono(id)
    if erro:
        return erro

    corpo = request.get_json()
    if 'nome' in corpo and not corpo['nome']:
        return jsonify({'erro': 'Informe o nome do título.'}), 400
    titulo.nome = corpo.get('nome', titulo.nome)
    titulo.data_lancamento = corpo.get('data_lancamento', titulo.data_lancamento)
    titulo.estado_conservacao = corpo.get('estado_conservacao', titulo.estado_conservacao)
    titulo.descricao = corpo.get('descricao', titulo.descricao)

    if 'autores' in corpo:
        autores = buscar_lista(Autor, corpo['autores'])
        if autores is None:
            return jsonify({'erro': 'Autor não encontrado.'}), 404
        for autor in list(titulo.autores):
            if autor not in autores:
                titulo.remover_autor(autor)
        for autor in autores:
            titulo.adicionar_autor(autor)

    if 'generos' in corpo:
        generos = buscar_lista(Genero, corpo['generos'])
        if generos is None:
            return jsonify({'erro': 'Gênero não encontrado.'}), 404
        for genero in list(titulo.generos):
            if genero not in generos:
                titulo.remover_genero(genero)
        for genero in generos:
            titulo.adicionar_genero(genero)

    titulo.salvar()
    return jsonify(titulo_para_json(titulo)), 200

@bp_titulo.route("/<int:id>", methods=['DELETE'])
def remover(id):
    titulo, erro = buscar_do_dono(id)
    if erro:
        return erro

    try:
        titulo.remover()
    except ValueError as erro:
        return jsonify({'erro': str(erro)}), 400
    return jsonify({'mensagem': 'Título removido.'}), 200

@bp_titulo.route("/<int:id>/autores/<int:autor_id>", methods=['POST'])
def adicionar_autor(id, autor_id):
    titulo, erro = buscar_do_dono(id)
    if erro:
        return erro
    autor = Autor.buscar(autor_id)
    if autor is None:
        return jsonify({'erro': 'Autor não encontrado.'}), 404

    titulo.adicionar_autor(autor)
    titulo.salvar()
    return jsonify(titulo_para_json(titulo)), 200

@bp_titulo.route("/<int:id>/autores/<int:autor_id>", methods=['DELETE'])
def remover_autor(id, autor_id):
    titulo, erro = buscar_do_dono(id)
    if erro:
        return erro
    autor = Autor.buscar(autor_id)
    if autor is None:
        return jsonify({'erro': 'Autor não encontrado.'}), 404

    titulo.remover_autor(autor)
    titulo.salvar()
    return jsonify(titulo_para_json(titulo)), 200

@bp_titulo.route("/<int:id>/generos/<int:genero_id>", methods=['POST'])
def adicionar_genero(id, genero_id):
    titulo, erro = buscar_do_dono(id)
    if erro:
        return erro
    genero = Genero.buscar(genero_id)
    if genero is None:
        return jsonify({'erro': 'Gênero não encontrado.'}), 404

    titulo.adicionar_genero(genero)
    titulo.salvar()
    return jsonify(titulo_para_json(titulo)), 200

@bp_titulo.route("/<int:id>/generos/<int:genero_id>", methods=['DELETE'])
def remover_genero(id, genero_id):
    titulo, erro = buscar_do_dono(id)
    if erro:
        return erro
    genero = Genero.buscar(genero_id)
    if genero is None:
        return jsonify({'erro': 'Gênero não encontrado.'}), 404

    titulo.remover_genero(genero)
    titulo.salvar()
    return jsonify(titulo_para_json(titulo)), 200
