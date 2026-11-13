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
            self.__Conectar()
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


    def __Conectar(self):
        try:
            self.connection = sqlite3.connect(self.__caminho)
            self.connection.row_factory = sqlite3.Row  
            self.connection.execute("PRAGMA foreign_keys = ON")

        except Exception as e:
            print("[Banco] erro ao conectar: ", e)
            raise


    def Desconectar(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    def Executar(self, comando:str, parameters: Iterable[Any]|dict = (), busca:bool = True):

        try:
            self.__Conectar()
            cursor = self.connection.cursor()

            cursor.execute(comando, parameters)

            if(busca == True and cursor.description is not None):
                return [dict(row) for row in cursor.fetchall()]

            else:
                self.connection.commit()
                return {"status":"ok", "rows_afetadas": cursor.rowcount, "id": cursor.lastrowid}

        except Exception as e:
            print("[Banco] erro ao executar comando: ", e)
            raise

        finally:
            self.Desconectar()