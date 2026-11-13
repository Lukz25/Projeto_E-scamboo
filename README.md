# E-scamboo

Plataforma web para troca de livros entre usuários. Cada pessoa cadastra os títulos que possui, pode marcar favoritos, e propor trocas: o interessado escolhe um título de outro usuário e oferece um ou mais dos seus próprios títulos em troca. Quando a proposta é aceita, os títulos trocam de dono.

## Funcionalidades

- **Cadastro e login** de usuários, com senha armazenada como hash SHA-256.
- **Acervo de livros** (títulos) com nome, autores, gêneros, data de lançamento, estado de conservação e descrição. Somente o dono pode editar ou remover um título.
- **Autores e gêneros** cadastrados e reutilizados entre os títulos. Autores e gêneros só podem ser removidos quando não há títulos vinculados a eles.
- **Favoritos**: cada usuário pode marcar títulos de outras pessoas como favoritos.
- **Propostas de troca**: o interessado propõe uma troca com uma observação. O dono do título desejado pode aceitar ou recusar. O interessado pode cancelar enquanto a proposta estiver pendente.
- **Remoção lógica (soft delete)**: registros não são apagados do banco; recebem `ativo = 0`.

## Tecnologias

- Backend: Python com Flask (`Flask==3.1.3`), organizado em blueprints.
- Banco de dados: SQLite, criado automaticamente na primeira execução.
- Frontend: páginas HTML, CSS e JavaScript puro, servidas pelo próprio Flask a partir da pasta `interface/`.
- Testes: `unittest` da biblioteca padrão.

## Estrutura do projeto

```
.
├── app.py                      # Ponto de entrada: cria o Flask, registra as rotas e inicializa o banco
├── requirements.txt            # Dependências Python
├── arquivoClasses/
│   ├── classes.py              # Modelos de domínio: Autor, Genero, Titulo, Usuario, Proposta
│   └── test_classes.py         # Testes unitários das classes
├── banco/
│   ├── classe_banco.py         # Acesso ao SQLite (Banco.Executar, inicialização)
│   └── script.sql              # Schema das tabelas, índices e dados de exemplo
├── rotas/
│   ├── routes_usuario.py       # Login, logout, usuários e favoritos
│   ├── routes_titulo.py        # Títulos e vínculos com autores e gêneros
│   ├── routes_autor.py         # Autores e vínculo com obras
│   ├── routes_genero.py        # Gêneros
│   └── routes_proposta.py      # Propostas de troca
└── interface/
    ├── login.html              # Entrada no sistema
    ├── livros.html             # Listagem de títulos
    ├── novo-livro.html / editar-livro.html
    ├── propor-troca.html       # Criação de proposta
    ├── propostas.html          # Acompanhamento e resposta de propostas
    ├── autores.html / generos.html / usuarios.html
    ├── css/                    # app.css e tema.css
    └── js/                     # comum.js (chamadas à API), livro-form.js, cadastro.js
```

## Como executar

Pré-requisito: Python 3.10 ou superior (o código usa anotações como `int | None`).

```bash
# 1. Crie e ative um ambiente virtual
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Inicie o servidor
python app.py
```

Depois, acesse `http://127.0.0.1:5000/` no navegador. A raiz redireciona para `livros.html`.

Na primeira execução, o arquivo `E-scamboo.db` é criado a partir de `banco/script.sql`, que também insere dados de exemplo. Para recriar o banco do zero, apague `E-scamboo.db` (e os arquivos `-wal` e `-shm`, se existirem) e reinicie a aplicação.

### Usuários de exemplo

| E-mail | Senha |
|---|---|
| ana@example.com | ana123 |
| bruno@example.com | bruno123 |
| carla@example.com | carla123 |
| diego@example.com | diego123 |

## Testes

Na raiz do projeto:

```bash
python -m unittest arquivoClasses.test_classes -v
```

O arquivo contém 28 testes para as regras de negócio das classes: vínculo de autores e gêneros aos títulos, favoritos, e o fluxo de propostas (criar, aceitar com troca de donos, recusar e cancelar).

## API

Todas as rotas retornam JSON. Rotas que alteram dados exigem login (sessão via cookie), exceto as de consulta pública.

### Usuário (`/usuario`)

| Método | Rota | Descrição |
|---|---|---|
| POST | `/usuario/Logar` | Login com `email` e `senha` |
| POST | `/usuario/Deslogar` | Encerra a sessão |
| GET | `/usuario/logado` | Dados do usuário logado |
| GET | `/usuario/` | Lista usuários |
| GET | `/usuario/<email>` | Dados de um usuário |
| POST | `/usuario/` | Cadastro |
| PUT | `/usuario/` | Atualiza o usuário logado |
| DELETE | `/usuario/` | Remove o usuário logado |
| POST | `/usuario/favoritos/<titulo_id>` | Favorita um título |
| DELETE | `/usuario/favoritos/<titulo_id>` | Remove dos favoritos |

### Títulos (`/titulo`)

| Método | Rota | Descrição |
|---|---|---|
| GET | `/titulo/` | Lista títulos. Aceita filtros `?autor=<id>` e `?genero=<id>` |
| GET | `/titulo/<id>` | Detalhes de um título |
| POST | `/titulo/` | Cadastra título (exige login) |
| PUT | `/titulo/<id>` | Atualiza título (somente o dono) |
| DELETE | `/titulo/<id>` | Remove título (somente o dono) |
| POST | `/titulo/<id>/autores/<autor_id>` | Vincula autor |
| DELETE | `/titulo/<id>/autores/<autor_id>` | Desvincula autor |
| POST | `/titulo/<id>/generos/<genero_id>` | Vincula gênero |
| DELETE | `/titulo/<id>/generos/<genero_id>` | Desvincula gênero |

### Autores (`/autor`) e gêneros (`/genero`)

Seguem o mesmo padrão: `GET /` (lista), `GET /<id>`, `POST /`, `PUT /<id>` e `DELETE /<id>`. Autores também aceitam `POST` e `DELETE` em `/autor/<id>/obras/<titulo_id>`.

### Propostas (`/proposta`)

| Método | Rota | Descrição |
|---|---|---|
| GET | `/proposta/` | Lista propostas |
| GET | `/proposta/<id>` | Detalhes de uma proposta |
| POST | `/proposta/` | Cria proposta (exige login). Corpo: `titulo_desejado`, `titulos_oferecidos` (lista de ids) e `observacao` |
| POST | `/proposta/<id>/aceitar` | Dono aceita; os títulos são trocados |
| POST | `/proposta/<id>/recusar` | Dono recusa |
| POST | `/proposta/<id>/cancelar` | Interessado cancela (somente se pendente) |

Situações possíveis de uma proposta: `pendente`, `aceita`, `recusada` e `cancelada`.

A pasta também traz a coleção `E-Scamboo.postman_collection.json`, que pode ser importada no Postman para testar essas rotas.

## Observações para desenvolvimento

- A chave de sessão (`app.secret_key`) está fixa no código de `app.py`. Para uso fora de ambiente de estudo, ela deve vir de variável de ambiente.
- O arquivo `E-scamboo.db` e a pasta `venv/` estão no `.gitignore` e não devem ser versionados.
- Para mudar o schema, altere `banco/script.sql` e recrie o banco, pois o script só roda quando o arquivo `.db` não existe.
