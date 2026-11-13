import sqlite3
from typing import Any, Iterable
import os

PASTA_PROJETO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Banco:

    def __init__(self):
        self.__caminho = os.path.join(PASTA_PROJETO, "E-scamboo.db")
        self.__script = os.path.join(PASTA_PROJETO, "banco", "script.sql")
        self.connection = None


    def inicializar_Banco(self):
        
        if os.path.exists(self.__caminho):
            print("[Banco] já existe, nada a fazer.")
            return
        
        try:
            self.connection = self.__Conectar()
            with open(self.__script, "r", encoding="utf-8") as f:
                self.connection.executescript(f.read())

            self.connection.commit()
            print("Banco criado e script executado com sucesso!")

        except Exception as e:
            print("[Banco] erro ao inicializar Banco: ", e)
            self.Desconectar()

            if os.path.exists(self.__caminho):
                os.remove(self.__caminho)

            for sufix in ("","-wal","-shm"):
                file = self.__caminho + sufix
                if os.path.exists(file):
                    os.remove(file)

            raise

        finally:
            self.Desconectar()


    def __Conectar(self) -> sqlite3.Connection:
        try:
            conexao = sqlite3.connect(self.__caminho)
            conexao.row_factory = sqlite3.Row
            conexao.execute("PRAGMA foreign_keys = ON")
            return conexao

        except Exception as e:
            print("[Banco] erro ao conectar: ", e)
            raise


    def Desconectar(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    # Cada chamada usa a sua própria conexão: o Flask atende várias requisições ao mesmo tempo
    def Executar(self, comando:str, parameters: Iterable[Any]|dict = (), busca:bool = True):

        conexao = self.__Conectar()
        try:
            cursor = conexao.cursor()

            cursor.execute(comando, parameters)

            if(busca == True and cursor.description is not None):
                return [dict(row) for row in cursor.fetchall()]

            else:
                conexao.commit()
                return {"status":"ok", "rows_afetadas": cursor.rowcount, "id": cursor.lastrowid}

        except Exception as e:
            print("[Banco] erro ao executar comando: ", e)
            raise

        finally:
            conexao.close()