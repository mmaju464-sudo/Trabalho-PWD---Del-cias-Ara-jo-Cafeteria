import sqlite3
import os


banco = os.path.join("instance", "ifitness.db")


if not os.path.exists(banco):
    print("ERRO: banco não encontrado!")
    print("Caminho:", banco)
    exit()


conexao = sqlite3.connect(banco)
cursor = conexao.cursor()


# Adiciona a coluna de pontos
try:
    cursor.execute("""
        ALTER TABLE usuarios
        ADD COLUMN pontos INTEGER NOT NULL DEFAULT 0
    """)
    print("Coluna pontos adicionada!")
except sqlite3.OperationalError:
    print("Coluna pontos já existe!")


# Adiciona a coluna de recompensa
try:
    cursor.execute("""
        ALTER TABLE usuarios
        ADD COLUMN recompensa_disponivel
        INTEGER NOT NULL DEFAULT 0
    """)
    print("Coluna recompensa_disponivel adicionada!")
except sqlite3.OperationalError:
    print("Coluna recompensa_disponivel já existe!")


conexao.commit()
conexao.close()


print("BANCO ATUALIZADO COM SUCESSO!")
print("Produtos e pedidos foram mantidos.")