import mysql.connector
from configurar import conexao

def ligar():
    return mysql.connector.connect(**conexao)
