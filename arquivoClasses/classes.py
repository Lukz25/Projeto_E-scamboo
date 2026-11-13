
from datetime import date
import hashlib
import sqlite3

from banco.classe_banco import Banco

banco = Banco()

class Autor:
    def __init__(self, id: int | None, nome: str):
        self.id = id
        self.nome = nome
        self.obras: list[Titulo] = []

    def adicionar_obra(self, titulo: "Titulo") -> None:
        if titulo not in self.obras:
            self.obras.append(titulo)
        if self not in titulo.autores:
            titulo.autores.append(self)

    def remover_obra(self, titulo: "Titulo") -> None:
        if titulo in self.obras:
            self.obras.remove(titulo)
        if self in titulo.autores:
            titulo.autores.remove(self)

    @classmethod
    def buscar(cls, id: int) -> "Autor | None":
        linhas = banco.Executar("SELECT id, nome FROM autor WHERE id = ? AND ativo = 1", (id,))
        if not linhas:
            return None
        autor = cls(linhas[0]['id'], linhas[0]['nome'])
        for linha in banco.Executar(
            "SELECT titulo.id FROM titulo JOIN autor_titulo ON autor_titulo.titulo = titulo.id "
            "WHERE autor_titulo.autor = ? AND titulo.ativo = 1 ORDER BY titulo.id", (id,)):
            autor.adicionar_obra(Titulo.buscar(linha['id']))
        return autor

    @classmethod
    def listar(cls) -> list["Autor"]:
        linhas = banco.Executar("SELECT id FROM autor WHERE ativo = 1 ORDER BY id")
        return [cls.buscar(linha['id']) for linha in linhas]

    def salvar(self) -> None:
        try:
            if self.id is None:
                self.id = banco.Executar("INSERT INTO autor (nome) VALUES (?)", (self.nome,))['id']
            else:
                banco.Executar("UPDATE autor SET nome = ? WHERE id = ?", (self.nome, self.id))
        except sqlite3.IntegrityError:
            raise ValueError("Já existe um autor com esse nome.")

    def remover(self) -> None:
        if self.obras:
            raise ValueError("Autor possui obras cadastradas.")
        banco.Executar("UPDATE autor SET ativo = 0 WHERE id = ?", (self.id,))

    def __eq__(self, outro) -> bool:
        if not isinstance(outro, Autor):
            return NotImplemented
        if self.id is None or outro.id is None:
            return self is outro
        return self.id == outro.id

    def __hash__(self) -> int:
        return hash(self.id) if self.id is not None else id(self)

    def __repr__(self) -> str:
        return f"Autor(id={self.id}, nome={self.nome})"


class Genero:
    def __init__(self, id: int | None, nome: str):
        self.id = id
        self.nome = nome

    @classmethod
    def buscar(cls, id: int) -> "Genero | None":
        linhas = banco.Executar("SELECT id, nome FROM genero WHERE id = ? AND ativo = 1", (id,))
        if not linhas:
            return None
        return cls(linhas[0]['id'], linhas[0]['nome'])

    @classmethod
    def listar(cls) -> list["Genero"]:
        linhas = banco.Executar("SELECT id, nome FROM genero WHERE ativo = 1 ORDER BY id")
        return [cls(linha['id'], linha['nome']) for linha in linhas]

    def salvar(self) -> None:
        try:
            if self.id is None:
                self.id = banco.Executar("INSERT INTO genero (nome) VALUES (?)", (self.nome,))['id']
            else:
                banco.Executar("UPDATE genero SET nome = ? WHERE id = ?", (self.nome, self.id))
        except sqlite3.IntegrityError:
            raise ValueError("Já existe um genero com esse nome.")

    def remover(self) -> None:
        linhas = banco.Executar(
            "SELECT COUNT(*) AS total FROM genero_titulo JOIN titulo ON titulo.id = genero_titulo.titulo "
            "WHERE genero_titulo.genero = ? AND titulo.ativo = 1", (self.id,))
        if linhas[0]['total'] > 0:
            raise ValueError("Genero possui títulos cadastrados.")
        banco.Executar("UPDATE genero SET ativo = 0 WHERE id = ?", (self.id,))

    def __eq__(self, outro) -> bool:
        if not isinstance(outro, Genero):
            return NotImplemented
        if self.id is None or outro.id is None:
            return self is outro
        return self.id == outro.id

    def __hash__(self) -> int:
        return hash(self.id) if self.id is not None else id(self)

    def __repr__(self) -> str:
        return f"Genero(id={self.id}, nome={self.nome})"


class Titulo:
    def __init__(
        self,
        id: int | None,
        nome: str,
        usuario: "Usuario",
        autores: list[Autor],
        generos: list[Genero],
        data_lancamento: str,
        estado_conservacao: str,
        descricao: str,
    ):
        self.id = id
        self.nome = nome
        self.usuario = usuario
        self.autores: list[Autor] = []
        self.generos: list[Genero] = []
        self.data_lancamento = data_lancamento
        self.estado_conservacao = estado_conservacao
        self.descricao = descricao
        for autor in autores:
            self.adicionar_autor(autor)
        for genero in generos:
            self.adicionar_genero(genero)
        usuario.adicionar_titulo_biblioteca(self)

    def adicionar_autor(self, autor: Autor) -> None:
        if autor not in self.autores:
            self.autores.append(autor)
        if self not in autor.obras:
            autor.obras.append(self)

    def remover_autor(self, autor: Autor) -> None:
        if autor in self.autores:
            self.autores.remove(autor)
        if self in autor.obras:
            autor.obras.remove(self)

    def adicionar_genero(self, genero: Genero) -> None:
        if genero not in self.generos:
            self.generos.append(genero)

    def remover_genero(self, genero: Genero) -> None:
        if genero in self.generos:
            self.generos.remove(genero)

    def possui_autor(self, autor: Autor) -> bool:
        return autor in self.autores

    def possui_genero(self, genero: Genero) -> bool:
        return genero in self.generos

    @classmethod
    def buscar(cls, id: int) -> "Titulo | None":
        linhas = banco.Executar("SELECT * FROM titulo WHERE id = ? AND ativo = 1", (id,))
        if not linhas:
            return None
        linha = linhas[0]
        dono = Usuario.montar(banco.Executar("SELECT * FROM usuario WHERE email = ?", (linha['usuario'],))[0])
        autores = [Autor(l['id'], l['nome']) for l in banco.Executar(
            "SELECT autor.id, autor.nome FROM autor JOIN autor_titulo ON autor_titulo.autor = autor.id "
            "WHERE autor_titulo.titulo = ? AND autor.ativo = 1 ORDER BY autor_titulo.id", (id,))]
        generos = [Genero(l['id'], l['nome']) for l in banco.Executar(
            "SELECT genero.id, genero.nome FROM genero JOIN genero_titulo ON genero_titulo.genero = genero.id "
            "WHERE genero_titulo.titulo = ? AND genero.ativo = 1 ORDER BY genero_titulo.id", (id,))]
        return cls(
            linha['id'],
            linha['nome'],
            dono,
            autores,
            generos,
            linha['data_lancamento'] or "",
            linha['estado_conservacao'] or "",
            linha['descricao'] or "",
        )

    @classmethod
    def listar(cls) -> list["Titulo"]:
        linhas = banco.Executar("SELECT id FROM titulo WHERE ativo = 1 ORDER BY id")
        return [cls.buscar(linha['id']) for linha in linhas]

    def salvar(self) -> None:
        if self.id is None:
            self.id = banco.Executar(
                "INSERT INTO titulo (nome, usuario, data_lancamento, estado_conservacao, descricao) VALUES (?, ?, ?, ?, ?)",
                (self.nome, self.usuario.get_email(), self.data_lancamento, self.estado_conservacao, self.descricao),
            )['id']
        else:
            banco.Executar(
                "UPDATE titulo SET nome = ?, usuario = ?, data_lancamento = ?, estado_conservacao = ?, descricao = ? WHERE id = ?",
                (self.nome, self.usuario.get_email(), self.data_lancamento, self.estado_conservacao, self.descricao, self.id),
            )

        banco.Executar("DELETE FROM autor_titulo WHERE titulo = ?", (self.id,))
        for autor in self.autores:
            banco.Executar("INSERT INTO autor_titulo (titulo, autor) VALUES (?, ?)", (self.id, autor.id))
        banco.Executar("DELETE FROM genero_titulo WHERE titulo = ?", (self.id,))
        for genero in self.generos:
            banco.Executar("INSERT INTO genero_titulo (titulo, genero) VALUES (?, ?)", (self.id, genero.id))

    def remover(self) -> None:
        linhas = banco.Executar(
            "SELECT COUNT(*) AS total FROM proposta WHERE ativo = 1 AND situacao = 'pendente' "
            "AND (titulo_desejado = ? OR id IN (SELECT proposta FROM titulo_oferecido WHERE titulo = ?))",
            (self.id, self.id))
        if linhas[0]['total'] > 0:
            raise ValueError("Título está em uma proposta pendente.")
        banco.Executar("UPDATE titulo SET ativo = 0 WHERE id = ?", (self.id,))

    def __eq__(self, outro) -> bool:
        if not isinstance(outro, Titulo):
            return NotImplemented
        if self.id is None or outro.id is None:
            return self is outro
        return self.id == outro.id

    def __hash__(self) -> int:
        return hash(self.id) if self.id is not None else id(self)

    def __repr__(self) -> str:
        return f"Titulo(id={self.id}, nome={self.nome})"


class Usuario:
    def __init__(self, nome: str, email: str, senha_hash: str, telefone: str, cep: str):
        self.nome = nome
        self.set_email(email)
        self.__senha_hash = senha_hash
        self.telefone = telefone
        self.cep = cep
        self.biblioteca: list[Titulo] = []
        self.favoritos: list[Titulo] = []

    def get_email(self) -> str:
        return self.__email

    def set_email(self, novo_email: str) -> None:
        if "@" not in novo_email:
            raise ValueError("E-mail inválido.")
        self.__email = novo_email

    @staticmethod
    def gerar_hash(senha: str) -> str:
        return hashlib.sha256(senha.encode()).hexdigest()

    def verificar_senha(self, senha: str) -> bool:
        return Usuario.gerar_hash(senha) == self.__senha_hash

    def alterar_senha(self, nova_senha: str) -> None:
        if not nova_senha:
            raise ValueError("Senha inválida.")
        self.__senha_hash = Usuario.gerar_hash(nova_senha)

    def adicionar_titulo_biblioteca(self, titulo: Titulo) -> None:
        if titulo in self.biblioteca:
            raise ValueError("Título já está na biblioteca.")
        self.biblioteca.append(titulo)
        titulo.usuario = self

    def remover_titulo_biblioteca(self, titulo: Titulo) -> None:
        if titulo not in self.biblioteca:
            raise ValueError("Título não está na biblioteca.")
        self.biblioteca.remove(titulo)
        if titulo in self.favoritos:
            self.favoritos.remove(titulo)

    def possui_titulo(self, titulo: Titulo) -> bool:
        return titulo in self.biblioteca

    def favoritar_titulo(self, titulo: Titulo) -> None:
        if titulo not in self.favoritos:
            self.favoritos.append(titulo)

    def desfavoritar_titulo(self, titulo: Titulo) -> None:
        if titulo in self.favoritos:
            self.favoritos.remove(titulo)

    def fazer_proposta(
        self,
        titulo_desejado: Titulo,
        titulos_oferecidos: list[Titulo],
        observacao: str = "",
    ) -> "Proposta":
        if not titulos_oferecidos:
            raise ValueError("Informe ao menos um título oferecido.")
        for titulo in titulos_oferecidos:
            if titulo not in self.biblioteca:
                raise ValueError(f"Você não possui o título {titulo.nome}.")
        return Proposta(
            interessado=self,
            titulo_desejado=titulo_desejado,
            titulos_oferecidos=titulos_oferecidos,
            observacao=observacao,
            data_criacao=date.today(),
        )

    @classmethod
    def montar(cls, linha: dict) -> "Usuario":
        return cls(linha['nome'], linha['email'], linha['senha_hash'], linha['telefone'], linha['cep'])

    @classmethod
    def buscar(cls, email: str) -> "Usuario | None":
        linhas = banco.Executar("SELECT * FROM usuario WHERE email = ? AND ativo = 1", (email,))
        if not linhas:
            return None
        usuario = cls.montar(linhas[0])
        for linha in banco.Executar("SELECT id FROM titulo WHERE usuario = ? AND ativo = 1 ORDER BY id", (email,)):
            usuario.adicionar_titulo_biblioteca(Titulo.buscar(linha['id']))
        for linha in banco.Executar(
            "SELECT titulo.id FROM titulo JOIN favorito ON favorito.titulo = titulo.id "
            "WHERE favorito.usuario = ? AND titulo.ativo = 1 ORDER BY favorito.id", (email,)):
            usuario.favoritar_titulo(Titulo.buscar(linha['id']))
        return usuario

    @classmethod
    def listar(cls) -> list["Usuario"]:
        linhas = banco.Executar("SELECT email FROM usuario WHERE ativo = 1 ORDER BY rowid")
        return [cls.buscar(linha['email']) for linha in linhas]

    @staticmethod
    def email_cadastrado(email: str) -> bool:
        return len(banco.Executar("SELECT email FROM usuario WHERE email = ?", (email,))) > 0

    def salvar(self) -> None:
        email = self.get_email()
        if banco.Executar("SELECT email FROM usuario WHERE email = ?", (email,)):
            banco.Executar(
                "UPDATE usuario SET senha_hash = ?, nome = ?, telefone = ?, cep = ? WHERE email = ?",
                (self.__senha_hash, self.nome, self.telefone, self.cep, email),
            )
        else:
            banco.Executar(
                "INSERT INTO usuario (email, senha_hash, nome, telefone, cep) VALUES (?, ?, ?, ?, ?)",
                (email, self.__senha_hash, self.nome, self.telefone, self.cep),
            )

        banco.Executar("DELETE FROM favorito WHERE usuario = ?", (email,))
        for titulo in self.favoritos:
            banco.Executar("INSERT INTO favorito (usuario, titulo) VALUES (?, ?)", (email, titulo.id))

    def remover(self) -> None:
        if self.biblioteca:
            raise ValueError("Usuário possui títulos cadastrados.")
        banco.Executar("UPDATE usuario SET ativo = 0 WHERE email = ?", (self.get_email(),))

    def __eq__(self, outro) -> bool:
        if not isinstance(outro, Usuario):
            return NotImplemented
        return self.get_email() == outro.get_email()

    def __hash__(self) -> int:
        return hash(self.get_email())

    def __repr__(self) -> str:
        return f"Usuario(nome={self.nome})"


class Proposta:
    def __init__(
        self,
        interessado: Usuario,
        titulo_desejado: Titulo,
        titulos_oferecidos: list[Titulo],
        observacao: str,
        data_criacao: date,
    ):
        self.id: int | None = None
        self.interessado = interessado
        self.titulo_desejado = titulo_desejado
        self.titulos_oferecidos = titulos_oferecidos
        self.observacao = observacao
        self.data_criacao = data_criacao
        self.situacao = "pendente"

    def esta_pendente(self) -> bool:
        return self.situacao == "pendente"

    def aceitar_proposta(self, usuario: Usuario) -> None:
        self.__validar_dono(usuario)
        self.__trocar_titulos()
        self.situacao = "aceita"

    def recusar_proposta(self, usuario: Usuario) -> None:
        self.__validar_dono(usuario)
        self.situacao = "recusada"

    def cancelar_proposta(self, usuario: Usuario) -> None:
        if not self.esta_pendente():
            raise ValueError("A proposta não está pendente.")
        if usuario != self.interessado:
            raise ValueError("Apenas o interessado pode cancelar a proposta.")
        self.situacao = "cancelada"

    def __validar_dono(self, usuario: Usuario) -> None:
        if not self.esta_pendente():
            raise ValueError("A proposta não está pendente.")
        if usuario != self.titulo_desejado.usuario:
            raise ValueError("Apenas o dono do título pode responder a proposta.")

    def __trocar_titulos(self) -> None:
        dono = self.titulo_desejado.usuario
        for titulo in self.titulos_oferecidos:
            if titulo not in self.interessado.biblioteca:
                raise ValueError(f"Interessado não possui mais {titulo.nome}.")

        dono.remover_titulo_biblioteca(self.titulo_desejado)
        self.interessado.adicionar_titulo_biblioteca(self.titulo_desejado)
        for titulo in self.titulos_oferecidos:
            self.interessado.remover_titulo_biblioteca(titulo)
            dono.adicionar_titulo_biblioteca(titulo)

    @classmethod
    def buscar(cls, id: int) -> "Proposta | None":
        linhas = banco.Executar(
            "SELECT proposta.*, titulo.usuario AS dono FROM proposta JOIN titulo ON titulo.id = proposta.titulo_desejado "
            "WHERE proposta.id = ? AND proposta.ativo = 1 AND titulo.ativo = 1", (id,))
        if not linhas:
            return None
        linha = linhas[0]

        interessado = Usuario.buscar(linha['interessado'])
        dono = interessado if linha['dono'] == linha['interessado'] else Usuario.buscar(linha['dono'])
        if interessado is None or dono is None:
            return None
        livros = {titulo.id: titulo for titulo in dono.biblioteca + interessado.biblioteca}

        oferecidos = []
        for l in banco.Executar("SELECT titulo FROM titulo_oferecido WHERE proposta = ? ORDER BY id", (id,)):
            titulo = livros.get(l['titulo']) or Titulo.buscar(l['titulo'])
            if titulo is not None:
                oferecidos.append(titulo)

        proposta = cls(
            interessado,
            livros[linha['titulo_desejado']],
            oferecidos,
            linha['observacao'] or "",
            date.fromisoformat(linha['data_criacao'][:10]),
        )
        proposta.id = linha['id']
        proposta.situacao = linha['situacao']
        return proposta

    @classmethod
    def listar(cls) -> list["Proposta"]:
        linhas = banco.Executar("SELECT id FROM proposta WHERE ativo = 1 ORDER BY id")
        propostas = [cls.buscar(linha['id']) for linha in linhas]
        return [proposta for proposta in propostas if proposta is not None]

    def salvar(self) -> None:
        if self.id is None:
            self.id = banco.Executar(
                "INSERT INTO proposta (interessado, titulo_desejado, observacao, data_criacao, situacao) VALUES (?, ?, ?, ?, ?)",
                (self.interessado.get_email(), self.titulo_desejado.id, self.observacao, self.data_criacao.isoformat(), self.situacao),
            )['id']
            for titulo in self.titulos_oferecidos:
                banco.Executar("INSERT INTO titulo_oferecido (proposta, titulo) VALUES (?, ?)", (self.id, titulo.id))
        else:
            banco.Executar(
                "UPDATE proposta SET observacao = ?, situacao = ? WHERE id = ?",
                (self.observacao, self.situacao, self.id),
            )

        if self.situacao == "aceita":
            usuarios: list[Usuario] = []
            for titulo in [self.titulo_desejado] + self.titulos_oferecidos:
                titulo.salvar()
                if titulo.usuario not in usuarios:
                    usuarios.append(titulo.usuario)
            for usuario in usuarios:
                usuario.salvar()

    def __repr__(self) -> str:
        return f"Proposta(interessado={self.interessado.nome}, situacao={self.situacao})"
