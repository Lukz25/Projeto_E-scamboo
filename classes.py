
from datetime import date


class Autor:
    def __init__(self, id: int, nome: str):
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

    def __repr__(self) -> str:
        return f"Autor(id={self.id}, nome={self.nome})"


class Genero:
    def __init__(self, id: int, nome: str):
        self.id = id
        self.nome = nome

    def __repr__(self) -> str:
        return f"Genero(id={self.id}, nome={self.nome})"


class Titulo:
    def __init__(
        self,
        id: int,
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

    def __repr__(self) -> str:
        return f"Titulo(id={self.id}, nome={self.nome})"


class Usuario:
    def __init__(self, nome: str, email: str, telefone: str, cep: str):
        self.nome = nome
        self.set_email(email)
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
        if usuario is not self.interessado:
            raise ValueError("Apenas o interessado pode cancelar a proposta.")
        self.situacao = "cancelada"

    def __validar_dono(self, usuario: Usuario) -> None:
        if not self.esta_pendente():
            raise ValueError("A proposta não está pendente.")
        if usuario is not self.titulo_desejado.usuario:
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

    def __repr__(self) -> str:
        return f"Proposta(interessado={self.interessado.nome}, situacao={self.situacao})"
