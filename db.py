import mysql.connector
from mysql.connector import pooling
from flask import g

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "tech_store"
}

try:
    conexao_pool = pooling.MySQLConnectionPool(
        pool_name="tech_store_pool",
        pool_size=5,
        **db_config
    )
    print("Pool de conexões MySQL criado com sucesso!")
except mysql.connector.Error as err:
    print(f"Erro ao criar o pool de conexões: {err}")
    conexao_pool = None


def obter_conexao():
    if 'db_conexao' not in g:
        if conexao_pool:
            g.db_conexao = conexao_pool.get_connection()
        else:
            g.db_conexao = mysql.connector.connect(**db_config)
            
    return g.db_conexao


def fechar_conexao(exception=None):
    conexao = g.pop('db_conexao', None)
    
    if conexao is not None:
        conexao.close()