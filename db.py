import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

def conectar_banco():
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

def executar_select(query, params=None):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute(query, params or ())
    resultado = cursor.fetchall()
    cursor.close()
    conexao.close()
    return resultado

def executar_write(query, params=None):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute(query, params or ())
    conexao.commit()
    cursor.close()
    conexao.close()